#!/usr/bin/env python3
"""GKE remote-MCP token-refreshing reverse proxy.

Listens on a local port and forwards MCP traffic to one of
https://container.googleapis.com/mcp{,/read-only,/delete-tools}, injecting
a fresh GCP access token (fetched via `gcloud auth print-access-token`)
into the Authorization header on every request.

Run one instance per blast-radius scope:

  proxy.py --port 8081 --upstream-path /mcp                 # full
  proxy.py --port 8082 --upstream-path /mcp/read-only       # read-only
  proxy.py --port 8083 --upstream-path /mcp/delete-tools    # delete-only

Tokens are fetched per-request for simplicity; add caching if call
volume warrants. Binds 0.0.0.0 by default so agents in Docker
containers can reach via host.docker.internal — keep the host firewalled.
"""

import argparse
import logging
import subprocess

from aiohttp import ClientSession, ClientTimeout, web

UPSTREAM_HOST = "https://container.googleapis.com"
HOP_BY_HOP = {
    "host", "authorization", "content-length", "connection",
    "transfer-encoding", "keep-alive", "proxy-authenticate",
    "proxy-authorization", "te", "trailers", "upgrade",
}


def get_access_token() -> str:
    result = subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        capture_output=True, text=True, check=True,
    )
    return result.stdout.strip()


async def proxy(request: web.Request) -> web.StreamResponse:
    upstream_path = request.app["upstream_path"]
    upstream_url = f"{UPSTREAM_HOST}{upstream_path}"

    try:
        token = get_access_token()
    except subprocess.CalledProcessError as e:
        logging.error("gcloud token fetch failed: %s", e.stderr.strip())
        return web.json_response(
            {"error": f"failed to fetch GCP access token: {e.stderr.strip()}"},
            status=500,
        )
    except FileNotFoundError:
        return web.json_response(
            {"error": "gcloud not found on PATH; install Google Cloud SDK"},
            status=500,
        )

    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in HOP_BY_HOP
    }
    headers["Authorization"] = f"Bearer {token}"

    body = await request.read()

    timeout = ClientTimeout(total=None, sock_read=600)
    async with ClientSession(timeout=timeout) as session:
        async with session.request(
            method=request.method,
            url=upstream_url,
            headers=headers,
            data=body if body else None,
            allow_redirects=False,
        ) as upstream:
            response = web.StreamResponse(
                status=upstream.status,
                headers={
                    k: v for k, v in upstream.headers.items()
                    if k.lower() not in HOP_BY_HOP
                },
            )
            await response.prepare(request)
            async for chunk in upstream.content.iter_chunked(4096):
                await response.write(chunk)
            await response.write_eof()
            return response


def main() -> None:
    parser = argparse.ArgumentParser(
        description="GKE remote-MCP token-refreshing proxy",
    )
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument(
        "--upstream-path",
        required=True,
        choices=["/mcp", "/mcp/read-only", "/mcp/delete-tools"],
    )
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    app = web.Application()
    app["upstream_path"] = args.upstream_path
    app.router.add_route("*", "/{tail:.*}", proxy)

    logging.info(
        "listening on %s:%d -> %s%s",
        args.host, args.port, UPSTREAM_HOST, args.upstream_path,
    )
    web.run_app(app, host=args.host, port=args.port, print=None)


if __name__ == "__main__":
    main()
