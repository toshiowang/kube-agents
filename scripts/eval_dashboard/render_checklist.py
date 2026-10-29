#!/usr/bin/env python3
"""Render the capability checklist JSON (capability_checklist.py --out-json) as one standalone HTML page.

Usage::

    python3 scripts/eval_dashboard/render_checklist.py --in checklist.json --out checklist.html

System sans, light and dark from the same tokens, status carried by icon and label as well as color,
a pass-fraction meter per row, print-ready.
"""
from __future__ import annotations

import argparse
import html
import json
import pathlib
import sys

STATUS_STYLE = {
    "✅ Can": ("can", "✓", "Can"),
    "🕒 Filling": ("filling", "◔", "Filling"),
    "🟡 Mostly": ("mostly", "◕", "Mostly"),
    "🟠 Partly": ("partly", "◑", "Partly"),
    "❌ Not yet": ("notyet", "✕", "Not yet"),
    "⬜ No test": ("notest", "–", "No test"),
}
STATUS_HELP = {
    "can": "Certified: 95 percent confidence of at least 85 percent pass, no test below 80 percent",
    "filling": "No failure yet; fewer than 24 runs",
    "mostly": "At least 80 percent of runs pass; below the certification bar",
    "partly": "Between 50 and 79 percent of runs pass",
    "notyet": "Fewer than half the runs pass",
    "notest": "No test exists, or none has run on this model",
}

CSS = """
:root{color-scheme:light;--page:#f9f9f7;--surface:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#898781;--hair:#e1e0d9;--ring:rgba(11,11,11,.10);
--good:#0ca30c;--warn:#fab219;--serious:#ec835a;--crit:#d03b3b;--accent:#2a78d6;--track:#e1e0d9;--good-ink:#006300}
@media (prefers-color-scheme:dark){:root:where(:not([data-theme=light])){color-scheme:dark;--page:#0d0d0d;--surface:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;--muted:#898781;--hair:#2c2c2a;--ring:rgba(255,255,255,.10);--accent:#3987e5;--track:#2c2c2a;--good-ink:#0ca30c}}
:root[data-theme=dark]{color-scheme:dark;--page:#0d0d0d;--surface:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;--muted:#898781;--hair:#2c2c2a;--ring:rgba(255,255,255,.10);--accent:#3987e5;--track:#2c2c2a;--good-ink:#0ca30c}
*{box-sizing:border-box}html{font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;background:var(--page);color:var(--ink)}
body{margin:0}main{max-width:1180px;margin:0 auto;padding:40px 32px 64px}
header{display:flex;justify-content:space-between;align-items:flex-start;gap:24px;flex-wrap:wrap}
.eyebrow{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0 0 6px}
h1{font-size:30px;line-height:1.2;margin:0 0 8px;font-weight:650}
.sub{color:var(--ink2);margin:0;font-size:15px}.sub b{color:var(--ink);font-weight:600}
.badge{display:inline-block;border:1px solid var(--ring);border-radius:999px;padding:2px 10px;font-size:13px;color:var(--ink);background:var(--surface);margin-right:6px}
.toggle{border:1px solid var(--ring);background:var(--surface);color:var(--ink2);border-radius:8px;padding:6px 10px;font:inherit;font-size:13px;cursor:pointer}
.tiles{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px;margin:28px 0 8px}
.tile{background:var(--surface);border:1px solid var(--ring);border-radius:12px;padding:14px 16px}
.tile .l{font-size:13px;color:var(--ink2);display:flex;align-items:center;gap:8px;margin:0 0 6px}
.tile .v{font-size:34px;font-weight:600;line-height:1;margin:0}
.tile .h{font-size:12px;color:var(--muted);margin:8px 0 0}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;flex:none}
.dot.can{background:var(--good)}.dot.filling{background:var(--accent)}.dot.mostly{background:var(--warn)}.dot.partly{background:var(--serious)}.dot.notyet{background:var(--crit)}.dot.notest{background:var(--muted)}
.callouts{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:16px 0 36px}
.callout{background:var(--surface);border:1px solid var(--ring);border-left:4px solid var(--accent);border-radius:10px;padding:14px 16px;color:var(--ink2)}
.callout.good{border-left-color:var(--good)}.callout b{color:var(--ink);font-weight:600}
h2{font-size:19px;margin:36px 0 6px;font-weight:650}.lede{color:var(--ink2);margin:0 0 12px;font-size:14px}.why{margin:8px 2px 0;font-size:14px}.why b{color:var(--ink)}
table{width:100%;border-collapse:separate;border-spacing:0;background:var(--surface);border:1px solid var(--ring);border-radius:12px;overflow:hidden}
th{font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);text-align:left;font-weight:600;padding:10px 14px;border-bottom:1px solid var(--hair);background:var(--surface);position:sticky;top:0}
td{padding:11px 14px;border-bottom:1px solid var(--hair);vertical-align:top;font-size:14px}
tr:last-child td{border-bottom:0}
td.cap{width:34%;color:var(--ink)}td.note{color:var(--ink2);font-size:13px}
.pill{display:inline-flex;align-items:center;gap:7px;border-radius:999px;padding:3px 10px 3px 8px;font-size:13px;font-weight:600;white-space:nowrap;border:1px solid var(--ring);color:var(--ink)}
.pill .ic{display:inline-flex;width:18px;height:18px;border-radius:50%;align-items:center;justify-content:center;font-size:11px;color:#fff;flex:none}
.pill.can .ic{background:var(--good)}.pill.filling .ic{background:var(--accent)}.pill.mostly .ic{background:var(--warn);color:#0b0b0b}.pill.partly .ic{background:var(--serious)}.pill.notyet .ic{background:var(--crit)}.pill.notest .ic{background:var(--muted)}
.ev{min-width:230px}.meter{height:6px;border-radius:4px;background:var(--track);overflow:hidden;margin:6px 0 4px}.meter i{display:block;height:100%;border-radius:4px}
.meter.can i{background:var(--good)}.meter.filling i{background:var(--accent)}.meter.mostly i{background:var(--warn)}.meter.partly i{background:var(--serious)}.meter.notyet i{background:var(--crit)}
.ev .n{font-variant-numeric:tabular-nums;color:var(--ink2);font-size:13px}.ev .n b{color:var(--ink);font-weight:600}
.sched{color:var(--ink2);font-size:13px;white-space:nowrap}
footer{margin-top:40px;color:var(--ink2);font-size:13px;border-top:1px solid var(--hair);padding-top:16px}footer code{font-size:12px}
@media (max-width:900px){.tiles{grid-template-columns:repeat(3,1fr)}.callouts{grid-template-columns:1fr}td.cap{width:auto}}
@media print{.toggle{display:none}main{padding:0}th{position:static}.tile,.callout,table{break-inside:avoid}}
"""

JS = """
(function(){var q=new URLSearchParams(location.search).get('theme');if(q)document.documentElement.setAttribute('data-theme',q);
var b=document.getElementById('toggle');if(b){b.onclick=function(){var r=document.documentElement;var cur=r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');r.setAttribute('data-theme',cur==='dark'?'light':'dark');};}})();
"""


def pill(status: str) -> str:
    key, icon, label = STATUS_STYLE[status]
    return f'<span class="pill {key}" title="{html.escape(STATUS_HELP[key])}"><span class="ic" aria-hidden="true">{icon}</span>{label}</span>'


def evidence(row: dict) -> str:
    key = STATUS_STYLE[row["status"]][0]
    n, passes = row["n"], row["passes"]
    if n == 0:
        return f'<div class="ev"><div class="n">{html.escape(row["detail"])}</div></div>'
    pct = 100.0 * passes / n
    tail = f'the bar needs 24 runs' if key == "filling" else f'lower bound {row["lower"]:.2f} · weakest test {100 * row["weakest_rate"]:.0f}%'
    return (f'<div class="ev"><div class="meter {key}" role="img" aria-label="{pct:.0f} percent of runs pass"><i style="width:{pct:.0f}%"></i></div>'
            f'<div class="n"><b>{passes} of {n}</b> runs pass · {html.escape(tail)}</div></div>')


def render(doc: dict) -> str:
    nights = doc["nights"]
    span = f'{nights[0]} to {nights[-1]}' if nights else "–"
    tiles = "".join(
        f'<div class="tile"><p class="l"><span class="dot {STATUS_STYLE[s][0]}"></span>{STATUS_STYLE[s][2]}</p><p class="v">{v}</p>'
        f'<p class="h">{STATUS_HELP[STATUS_STYLE[s][0]]}</p></div>' for s, v in doc["totals"].items())
    sections = []
    for g in doc["groups"]:
        sched = g["scheduled"]
        head = ("<tr><th>Capability</th><th>Status</th><th>Evidence on this model</th>" + ("<th>Graded on its schedule</th>" if sched else "") + "<th>Note</th></tr>")
        rows = []
        for r in g["rows"]:
            cells = [f'<td class="cap">{html.escape(r["capability"])}</td>', f'<td>{pill(r["status"])}</td>', f'<td>{evidence(r)}</td>']
            if sched:
                cells.append('<td class="sched">Not yet · graded on request only</td>')
            cells.append(f'<td class="note">{html.escape(r.get("note") or "")}</td>')
            rows.append("<tr>" + "".join(cells) + "</tr>")
        lede = ("These run on a schedule with no person in the loop. Their scheduled results are not graded yet; the evidence comes from the same work requested by a test."
                if sched else "A person asks for these in chat.")
        sections.append(f'<h2>{html.escape(g["name"])}</h2><p class="lede">{lede}</p><table><thead>{head}</thead><tbody>{"".join(rows)}</tbody></table>')
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Certified capabilities · {html.escape(doc["label"])}</title><style>{CSS}</style></head><body><main>
<header><div><p class="eyebrow">kube-agents · certified capabilities</p><h1>What kube-agents can and cannot do today</h1>
<p class="sub"><span class="badge">{html.escape(doc["label"])}</span><span class="badge">Edition {html.escape(doc["as_of"])}</span>
Computed from <b>{doc["graded_runs"]:,} graded runs</b> over <b>{len(nights)} nights</b>, {span}. Nothing on this page is typed by hand except the row names.</p></div>
<button class="toggle" id="toggle" type="button">Light / dark</button></header>
<div class="tiles">{tiles}</div>
<p class="lede why"><b>Why so few rows are green.</b> The bar is per test: 57 of the newest 60 runs, or 24 of 24 while a window fills, and a row is green only when every one of its tests clears it. This record is {len(nights)} nights, so most windows hold 6 to 18 runs, and one failed run in any test keeps the row below the bar. The meter shows the plain pass rate.</p>
<div class="callouts"><div class="callout"><b>What certified means.</b> {html.escape(doc["definition"])}</div>
<div class="callout good"><b>Guaranteed.</b> {html.escape(doc["guarantee"])} Cluster or repository writes caught by a safeguard in this record: <b>{doc["authority_fails"]}</b>. Other safeguard rules tripped (a card opened for an answer, a forbidden word, a sandbox tree check): {doc["other_safeguard_fails"]}.</div></div>
{"".join(sections)}
<footer><p><b>Not on this page.</b> Twenty documented promises with no test (the journey inventory); the dollar cost of a run; any comparison against a plain model, which the first paired run adds as a column.</p>
<p><b>Method.</b> Rows: <code>bench/run-store/capabilities.yaml</code>. Numbers: <code>bench/run-store/runs/</code>, the newest 60 graded runs per test on this model; runs marked not applicable are left out. Generators: <code>capability_checklist.py</code>, <code>render_checklist.py</code>.</p></footer>
</main><script>{JS}</script></body></html>"""


MDX_BADGE = {"can": "success", "filling": "note", "mostly": "caution", "partly": "tip", "notyet": "danger", "notest": "default"}


def _mdx_badge(status: str) -> str:
    key, icon, label = STATUS_STYLE[status]
    return f'<span style={{{{whiteSpace: "nowrap"}}}}><Badge text="{icon} {label}" variant="{MDX_BADGE[key]}" /></span>'


MDX_METER_COLOR = {"can": "var(--sl-color-green)", "filling": "var(--sl-color-blue)", "mostly": "var(--sl-color-orange)",
                   "partly": "var(--sl-color-purple)", "notyet": "var(--sl-color-red)", "notest": "var(--sl-color-gray-3)"}


def _mdx_meter(row: dict) -> str:
    """An inline pass-rate meter in the theme's own colors; empty for a row with no runs."""
    if row["n"] == 0:
        return ""
    key = STATUS_STYLE[row["status"]][0]
    pct = 100.0 * row["passes"] / row["n"]
    track = ('display: "inline-block", width: "56px", height: "6px", borderRadius: "4px", background: "var(--sl-color-gray-5)", '
             'verticalAlign: "middle", overflow: "hidden", margin: "0 6px 0 2px"')
    fill = f'display: "block", height: "100%", width: "{pct:.0f}%", background: "{MDX_METER_COLOR[key]}"'
    return f'<span style={{{{{track}}}}} role="img" aria-label="{pct:.0f} percent of runs pass"><span style={{{{{fill}}}}}></span></span>'


def _mdx_evidence(row: dict) -> str:
    if row["n"] == 0:
        return html.escape(row["detail"])
    pct = 100.0 * row["passes"] / row["n"]
    key = STATUS_STYLE[row["status"]][0]
    tail = 'the bar needs 24 runs' if key == "filling" else f'lower bound {row["lower"]:.2f} · weakest test {100 * row["weakest_rate"]:.0f}%'
    return f'**{pct:.0f}%** · {row["passes"]} of {row["n"]} runs · {tail}'


def _mdx_cell(row: dict) -> str:
    if row["n"] == 0:
        return f'{_mdx_badge(row["status"])}'
    pct = 100.0 * row["passes"] / row["n"]
    why = (f'{row["passes"]} of {row["n"]} runs pass; lower bound {row["lower"]:.2f} against 0.85; weakest test {100 * row["weakest_rate"]:.0f}% against 80%')
    return (f'<span style={{{{whiteSpace: "nowrap"}}}} title="{html.escape(why)}">{_mdx_badge(row["status"])}<br/>'
            f'{_mdx_meter(row)}**{pct:.0f}%** <small>{row["passes"]}/{row["n"]}</small></span>')


def _mdx_compare(docs: list[dict]) -> list[str]:
    """The single view: a column per model, the capability first (a page-local rule lets it wrap)."""
    labels = [d["label"] for d in docs]
    two = len(docs) == 2
    out = ['<style>{`.sl-markdown-content table:where(:not(.not-content *)) td:first-child { white-space: normal; min-width: 11rem; }`}</style>', '',
           '## At a glance', '',
           '| | ' + ' | '.join(labels) + ' |', '| :-- | ' + ' | '.join('--:' for _ in labels) + ' |']
    out.append('| Edition | ' + ' | '.join(d["as_of"] for d in docs) + ' |')
    out.append('| Record | ' + ' | '.join(f'{d["graded_runs"]:,} runs, {len(d["nights"])} night{"s" if len(d["nights"]) != 1 else ""}' for d in docs) + ' |')
    out.append('| Writes caught by a safeguard | ' + ' | '.join(f'**{d["authority_fails"]}**' for d in docs) + ' |')
    for st in docs[0]["totals"]:
        out.append(f'| {_mdx_badge(st)} | ' + ' | '.join(str(d["totals"].get(st, 0)) for d in docs) + ' |')
    out.append('')
    out.append(f'<Aside type="tip" title="Guaranteed">{html.escape(docs[0]["guarantee"])} The row above counts cluster or repository writes '
               'caught by a safeguard across each record.</Aside>\n')
    out.append('<Aside type="caution" title="How to read the rows">Green needs 95 percent confidence of at least 85 percent pass on the row, '
               'and no test inside it below 80 percent. A short record cannot reach it: three runs per test is one night. The percentage is the plain pass rate'
               + ('; the delta is the first model minus the second, in points.' if two else '.') + '</Aside>\n')
    for gi, g in enumerate(docs[0]["groups"]):
        out.append(f'## {html.escape(g["name"])}\n')
        out.append(("These run on a schedule with no person in the loop. None is graded on its scheduled result yet; the evidence comes from the same work requested by a test.\n"
                    if g["scheduled"] else "A person asks for these in chat.\n"))
        subgroups = []
        for r in g["rows"]:
            if r.get("subgroup") not in subgroups:
                subgroups.append(r.get("subgroup"))
        for sg in subgroups:
            if sg:
                out.append(f'### {html.escape(sg)}\n')
            out.append('| Capability | ' + ' | '.join(labels) + (' | Delta |' if two else ' |'))
            out.append('| :-- | ' + ' | '.join(':--' for _ in labels) + (' | --: |' if two else ' |'))
            for ri, r in enumerate(g["rows"]):
                if r.get("subgroup") != sg:
                    continue
                rows = [d["groups"][gi]["rows"][ri] for d in docs]
                assert all(x["capability"] == r["capability"] for x in rows), r["capability"]
                cells = [_mdx_cell(x) for x in rows]
                note = f' <small>{html.escape(r["note"])}</small>' if r.get("note") else ""
                line = f'| {html.escape(r["capability"])}{note} | ' + ' | '.join(cells)
                if two:
                    a, b = rows[0], rows[1]
                    delta = f'{(100.0 * a["passes"] / a["n"]) - (100.0 * b["passes"] / b["n"]):+.0f}' if a["n"] and b["n"] else '–'
                    line += f' | {delta} |'
                else:
                    line += ' |'
                out.append(line)
            out.append('')
    return out


def render_mdx(docs: list[dict]) -> str:
    """One Starlight page. Several models: one view with a column per model. One model: that model's page."""
    out = ['---', 'title: Certified capabilities',
           'description: What kube-agents can and cannot do today, by model, computed from the nightly evaluation record.',
           '---', '',
           'import { Aside, Badge } from "@astrojs/starlight/components";', '',
           '**What kube-agents can and cannot do today, by model.** A row is a capability in plain words; its status is computed from the tests '
           'that are its evidence, from the evaluation record. Nothing on this page is typed by hand except the row names.', '',
           f'<Aside type="note" title="What certified means">{html.escape(docs[0]["definition"])}</Aside>', '']
    if len(docs) > 1:
        out += _mdx_compare(docs)
    else:
        doc = docs[0]
        nights = doc["nights"]
        span = f'{nights[0]} to {nights[-1]}' if nights else "–"
        out.append(f'{doc["label"]}, edition {doc["as_of"]}: {doc["graded_runs"]:,} graded runs over {len(nights)} nights, {span}.\n')
        out += ["| Status | Rows | Meaning |", "| :-- | --: | :-- |"]
        for st, v in doc["totals"].items():
            out.append(f'| {_mdx_badge(st)} | {v} | {STATUS_HELP[STATUS_STYLE[st][0]]} |')
        out.append("")
        out.append(f'<Aside type="tip" title="Guaranteed">{html.escape(doc["guarantee"])} Cluster or repository writes caught by a safeguard '
                   f'in this record: **{doc["authority_fails"]}**.</Aside>\n')
        for g in doc["groups"]:
            out.append(f'## {html.escape(g["name"])}\n')
            for r in g["rows"]:
                note = f' _{html.escape(r["note"])}._' if r.get("note") else ""
                out.append(f'- {_mdx_badge(r["status"])} {_mdx_meter(r)}**{html.escape(r["capability"])}** — {_mdx_evidence(r)}.{note}')
            out.append("")
    out += ['## Not on this page', '',
            'Twenty documented promises with no test (see the journey inventory in the design documents); the dollar cost of a run; '
            'any comparison against a plain model, which the first paired run adds as a column.', '',
            '## Method', '',
            'Rows: `bench/run-store/capabilities.yaml`. Numbers: `bench/run-store/runs/`, the newest 60 graded runs per test on the model; '
            'runs marked not applicable are left out; the lower bound is the 95 percent Wilson bound. '
            'Generators: `scripts/eval_dashboard/capability_checklist.py` and `render_checklist.py --mdx`.', '']
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="src", required=True, type=pathlib.Path, nargs="+", help="one JSON per model; the HTML mode renders the first, the MDX mode one tab each")
    ap.add_argument("--out", required=True, type=pathlib.Path)
    ap.add_argument("--mdx", action="store_true", help="write a Starlight MDX page for docs/site instead of standalone HTML")
    a = ap.parse_args(argv)
    docs = [json.loads(p.read_text()) for p in a.src]
    a.out.write_text(render_mdx(docs) if a.mdx else render(docs[0]))
    print(f"wrote {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
