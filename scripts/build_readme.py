#!/usr/bin/env python3
"""Build the terminal-workflow profile README.

The hero is one animated SVG drawn to look like Aziz's real setup, read from
github.com/azizu06/dotfiles:

  * Ghostty window, Catppuccin Mocha theme, JetBrainsMono Nerd Font, padding 10x8
  * herdr multiplexer (sidebar toggled off): tab row on top, blue border on
    the focused pane
  * left pane: LazyVim (catppuccin mocha, lualine, relative numbers)
  * right pane: zsh with oh-my-zsh robbyrussell prompt and conda's (base)

GitHub strips CSS and JS from Markdown, but CSS and SMIL inside an SVG <img>
still run, so the motion is SMIL. Every asset has four variants (desktop
dark/light, mobile dark/light) picked by <picture> media queries. Light uses
Catppuccin Latte.

    python3 scripts/build_readme.py

Content comes from the README on main and Aziz's verified project notes.
Do not add numbers that are not there.
"""

from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# Cursor blink. His Ghostty config has cursor-style-blink = false, but the
# README reads better with a blinking block, so looks win here.
BLINK = True

# ---------------------------------------------------------------------------
# THEMES: Catppuccin Mocha (his Ghostty, herdr and Neovim theme) and Latte
# ---------------------------------------------------------------------------

MOCHA = dict(
    rosewater="#f5e0dc", flamingo="#f2cdcd", pink="#f5c2e7", mauve="#cba6f7",
    red="#f38ba8", maroon="#eba0ac", peach="#fab387", yellow="#f9e2af",
    green="#a6e3a1", teal="#94e2d5", sky="#89dceb", sapphire="#74c7ec",
    blue="#89b4fa", lavender="#b4befe", text="#cdd6f4", subtext1="#bac2de",
    subtext0="#a6adc8", overlay2="#9399b2", overlay1="#7f849c", overlay0="#6c7086",
    surface2="#585b70", surface1="#45475a", surface0="#313244", base="#1e1e2e",
    mantle="#181825", crust="#11111b", cursorline="#2a2b3c", frame="#3a3b4f",
)
LATTE = dict(
    rosewater="#dc8a78", flamingo="#dd7878", pink="#ea76cb", mauve="#8839ef",
    red="#d20f39", maroon="#e64553", peach="#fe640b", yellow="#df8e1d",
    green="#40a02b", teal="#179299", sky="#04a5e5", sapphire="#209fb5",
    blue="#1e66f5", lavender="#7287fd", text="#4c4f69", subtext1="#5c5f77",
    subtext0="#6c6f85", overlay2="#7c7f93", overlay1="#8c8fa1", overlay0="#9ca0b0",
    surface2="#acb0be", surface1="#bcc0cc", surface0="#ccd0da", base="#eff1f5",
    mantle="#e6e9ef", crust="#dce0e8", cursorline="#e4e7ef", frame="#c9cdd8",
)
THEMES = {"dark": MOCHA, "light": LATTE}

MONO = ("'JetBrainsMono Nerd Font','JetBrains Mono',ui-monospace,SFMono-Regular,"
        "'SF Mono',Menlo,Consolas,'Liberation Mono',monospace")
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

# ---------------------------------------------------------------------------
# CONTENT
# ---------------------------------------------------------------------------

LINKS = [
    ("azizu.dev", "https://azizu.dev", "Portfolio: azizu.dev"),
    ("linkedin", "https://linkedin.com/in/abduaziz-umarov", "LinkedIn: abduaziz-umarov"),
    ("devpost", "https://devpost.com/azizu06", "Devpost: azizu06"),
]

# aziz.lua, the Neovim buffer. Tokens: (text, color-key). Key "k" = keyword,
# "f" = field, "s" = string, "o" = operator, "p" = punctuation, "c" = comment,
# "v" = variable.
def _kv(key, val_tokens, width=7):
    return [("  ", "v"), (key.ljust(width), "f"), ("= ", "o")] + val_tokens + [(",", "p")]


def _s(x):
    return ("\"" + x + "\"", "s")


def _list(*items):
    toks = [("{ ", "p")]
    for i, it in enumerate(items):
        toks.append(_s(it))
        if i < len(items) - 1:
            toks.append((", ", "p"))
    toks.append((" }", "p"))
    return toks


BUFFER = [
    [("-- aziz.lua", "c")],
    [("local ", "k"), ("aziz ", "v"), ("= ", "o"), ("{", "p")],
    _kv("name", [_s("Abduaziz Umarov")]),
    _kv("school", [_s("UCF CS, May 2028")]),
    _kv("role", [_s("SWE Intern")]),
    _kv("at", [_s("Versant Media")]),
    _kv("team", [_s("Rotten Tomatoes")]),
    _kv("builds", _list("backend", "AI")),
    _kv("oss", [_s("badges/shields")]),
    _kv("setup", _list("herdr", "nvim")),
    _kv("seeks", [_s("Summer '27 SWE intern")]),
    _kv("afk", [_s("chess, hackathons")]),
    [("}", "p")],
    [],
    [("return ", "k"), ("aziz", "v")],
]
BUFFER_NAME = "aziz.lua"

# Shell script: each step is (command, output-lines). Output lines are token
# lists. A step may also change the prompt directory.
B = "dirb"  # tree directory color (tree default di=01;34, bold blue)
LSDIR = "teal b"  # oh-my-zsh LSCOLORS "Gxfx...": directories bold cyan

LS_PROJECTS = ["backrooms", "crisislens", "farsight", "shields", "snaplist"]

WINS_DESK = [
    ("crisislens", "Databricks 1st · Hacklytics 2026"),
    ("farsight", "4 sponsor tracks · Knight Hacks IX"),
    ("backrooms", "Hyphenate track prize · Cal Hacks 13.0"),
]
WINS_MOB = [
    ("crisislens", "1st · Databricks · Hacklytics '26"),
    ("farsight", "4 sponsor tracks · Knight Hacks IX"),
    ("backrooms", "Hyphenate prize · Cal Hacks 13.0"),
]

# Real merged PRs: gh pr list -R badges/shields -A azizu06 -s merged
SHIELDS_PRS = [
    ("#12064", "[Dynamic Endpoint] Allow self-hosters to disable open-ended badges"),
    ("#12026", "[GithubIssues GithubPullRequests] Add draft filters without changing unfiltered counts"),
    ("#11945", "[AzureDevops] Make the build badge send the PAT so it works on private projects"),
]

# Real top level of github.com/azizu06/dotfiles (tree hides dotfiles).
DOTFILES = [
    ("AGENTS.md", "f"), ("Brewfile", "f"), ("CLAUDE.md", "f"), ("GEMINI.md", "f"),
    ("README.md", "f"), ("agents", "d"), ("bin", "d"), ("claude-setup", "d"),
    ("cmux", "d"), ("firstmate", "d"), ("ghostty", "d"), ("herdr", "d"),
    ("install.sh", "x"), ("karabiner", "d"), ("macos", "d"), ("nvim", "d"),
    ("sync.sh", "x"), ("tests", "d"), ("zsh", "d"),
]

PROJECTS = [
    {
        "slug": "crisislens", "dir": "crisislens",
        "url": "https://github.com/azizu06/CrisisLensV2",
        "repo": "github.com/azizu06/CrisisLensV2",
        "win": "1st place · Databricks Challenge · Hacklytics 2026 · 234 projects",
        "win_m": "1st · Databricks Challenge · Hacklytics 2026",
        "desc": ("AI dashboard that ranks countries by crisis risk on a 3D globe, "
                 "with Databricks Genie for plain-English questions."),
        "extra": ("demo video", "https://youtu.be/YD6H3emkDrc"),
    },
    {
        "slug": "farsight", "dir": "farsight",
        "url": "https://github.com/azizu06/farsight",
        "repo": "github.com/azizu06/farsight",
        "win": "won 4 sponsor tracks · Knight Hacks IX · 212 projects",
        "win_m": "4 sponsor tracks · Knight Hacks IX",
        "desc": ("Search-and-rescue rover you drive from a Meta Quest headset, with "
                 "live LiDAR video and person detection running on a Jetson Orin Nano."),
        "extra": ("demo video", "https://youtu.be/AmrOGcTBTKU"),
    },
    {
        "slug": "backrooms", "dir": "backrooms",
        "url": "https://github.com/azizu06/backrooms",
        "repo": "github.com/azizu06/backrooms",
        "win": "Hyphenate track prize · Cal Hacks 13.0 · 652 projects",
        "win_m": "Hyphenate track prize · Cal Hacks 13.0",
        "desc": ("A back office where Claude Agent SDK agents do a small business's "
                 "finance work, and a 28-rule policy engine plus passkey approvals "
                 "stop them from moving money they shouldn't."),
        "extra": ("demo video", "https://youtu.be/dm1FlQTZYT8"),
    },
    {
        "slug": "shields", "dir": "shields",
        "url": "https://github.com/badges/shields/pulls?q=is%3Apr+author%3Aazizu06+is%3Amerged",
        "repo": "github.com/badges/shields",
        "win": "open source · 3 merged PRs",
        "win_m": "open source · 3 merged PRs",
        "desc": ("Contributor to the 27,000+ star service behind README badges: "
                 "Azure DevOps auth, draft-PR filters on GitHub badges, and an "
                 "SSRF fix across 7 badge routes."),
        "extra": None,
    },
    {
        "slug": "snaplist", "dir": "snaplist",
        "url": "https://github.com/azizu06/snaplist",
        "repo": "github.com/azizu06/snaplist",
        "win": "solo build · iOS",
        "win_m": "solo build · iOS",
        "desc": ("iPhone app I built solo that turns photos of a used item into a "
                 "priced, ready-to-post resale listing. SwiftUI, TypeScript, Supabase."),
        "extra": None,
    },
]

# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def f(n: float) -> str:
    return f"{n:.2f}".rstrip("0").rstrip(".")


TOKEN_CLASS = {
    "k": "mauve", "f": "lavender", "s": "green", "o": "sky", "p": "overlay2",
    "c": "overlay2 i", "v": "text", "dirb": "blue b", "d": "blue b", "x": "green b",
    "t": "text", "dim": "overlay1", "mut": "subtext0",
}


def _lum(hx):
    r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5))
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def _mix(a, b, k):
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * k):02x}" for x, y in zip(ca, cb))


BG_KEYS = {"base", "mantle", "crust", "surface0", "cursorline", "frame"}
MIN_CONTRAST = 4.8  # WCAG AA is 4.5; margin for text on mantle/surface0 bars


def readable(t: dict) -> dict:
    """Push every text color toward the theme's text color until it clears
    MIN_CONTRAST against the background. Background keys stay as they are."""
    out = dict(t)
    toward = "#000000" if _lum(t["base"]) > 0.5 else "#ffffff"  # keep hue, add contrast
    for k, v in t.items():
        if k in BG_KEYS:
            continue
        c, step = v, 0
        while contrast(c, t["base"]) < MIN_CONTRAST and step < 40:
            step += 1
            c = _mix(v, toward, step / 40)
        out[k] = c
    return out


def style_block(t: dict, size: float) -> str:
    t = readable(t)
    rules = [f".m{{font-family:{MONO};font-size:{f(size)}px;white-space:pre}}",
             f".s{{font-family:{SANS}}}", ".b{font-weight:700}", ".i{font-style:italic}"]
    for k, v in t.items():
        rules.append(f".{k}{{fill:{v}}}")
    return "<style>" + "".join(rules) + "</style>"


def svg_doc(w, h, t, size, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">'
            f"<title>{esc(title)}</title>{style_block(t, size)}{body}</svg>")


def tline(x0, y, cw, tokens, col0=0):
    """One terminal row. Each token sits on its own column so syntax colors
    stay aligned whatever monospace font the viewer has."""
    out, col = [], col0
    for text, key in tokens:
        if text.strip():
            cls = TOKEN_CLASS.get(key, key)
            lead = len(text) - len(text.lstrip(" "))
            out.append(f'<text x="{f(x0 + (col + lead) * cw)}" y="{f(y)}" class="m {cls}">'
                       f"{esc(text.strip(' '))}</text>")
        col += len(text)
    return "".join(out)


def tlen(tokens) -> int:
    return sum(len(t) for t, _ in tokens)


class Timeline:
    """All animations share one duration D, so they stay in sync forever."""

    def __init__(self, D: float):
        self.D = D

    def kt(self, times):
        return ";".join(f"{min(max(x / self.D, 0), 1):.4f}" for x in times)

    def _norm(self, pts, initial):
        pts = sorted(pts, key=lambda p: p[0])
        out = [(0.0, initial)]
        for tm, v in pts:
            tm = round(tm, 3)
            if tm <= 0:
                out[0] = (0.0, v)
            elif out[-1][0] == tm:
                out[-1] = (tm, v)
            else:
                out.append((tm, v))
        return out

    def discrete(self, attr, pts, initial):
        pts = self._norm(pts, initial)
        vals = ";".join(str(v) for _, v in pts)
        return (f'<animate attributeName="{attr}" dur="{self.D}s" repeatCount="indefinite" '
                f'calcMode="discrete" values="{vals}" keyTimes="{self.kt([p[0] for p in pts])}"/>')

    def translate(self, pts, initial):
        pts = self._norm(pts, initial)
        vals = ";".join(f"{f(x)},{f(y)}" for _, (x, y) in pts)
        return (f'<animateTransform attributeName="transform" type="translate" dur="{self.D}s" '
                f'repeatCount="indefinite" calcMode="discrete" values="{vals}" '
                f'keyTimes="{self.kt([p[0] for p in pts])}"/>')

    def shown(self, intervals, body, static_t=None):
        """Group visible only during the given (start, end) intervals."""
        pts = []
        for a, b in intervals:
            pts.append((a, 1))
            if b < self.D:
                pts.append((b, 0))
        st = self.D - 0.01 if static_t is None else static_t
        base = 1 if any(a <= st < b for a, b in intervals) else 0
        return f'<g opacity="{base}">{self.discrete("opacity", pts, 0)}{body}</g>'


def blink(body):
    if not BLINK:
        return body
    return ('<g><animate attributeName="opacity" dur="1.1s" repeatCount="indefinite" '
            f'calcMode="discrete" values="1;0" keyTimes="0;0.55"/>{body}</g>')


def traffic_lights(x, y):
    cols = ["#ff5f57", "#febc2e", "#28c840"]
    return "".join(f'<circle cx="{x + i * 20}" cy="{y}" r="6" fill="{c}"/>' for i, c in enumerate(cols))


# ---------------------------------------------------------------------------
# Shell session (shared by desktop and mobile)
# ---------------------------------------------------------------------------


def prompt_tokens(where: str):
    toks = [("(base) ", "t"), ("➜  ", "green b"), (where, "teal b")]
    if where != "~":
        toks += [(" git:(", "blue b"), ("main", "red"), (")", "blue b")]
    return toks + [(" ", "t")]


def ls_columns(names, width):
    """BSD ls -C: column-major, fewest rows that fit the width."""
    for rows in range(1, len(names) + 1):
        cols = [names[i:i + rows] for i in range(0, len(names), rows)]
        widths = [max(len(n) for n in c) + 2 for c in cols]
        if sum(widths) - 2 <= width:
            lines = []
            for r in range(rows):
                toks = []
                for ci, c in enumerate(cols):
                    if r < len(c):
                        toks.append((c[r].ljust(widths[ci]) if ci < len(cols) - 1 else c[r], LSDIR))
                lines.append(toks)
            return lines
    raise ValueError("ls does not fit")


def gh_lines(width):
    out = []
    for num, title in SHIELDS_PRS:
        room = width - len(num) - 2
        t = title if len(title) <= room else title[: room - 1].rstrip() + "…"
        out.append([(num, "mauve"), ("  ", "t"), (t, "t")])
    return out


def tree_lines():
    out = [[(".", B)]]
    for i, (name, kind) in enumerate(DOTFILES):
        branch = "└── " if i == len(DOTFILES) - 1 else "├── "
        out.append([(branch, "overlay1"), (name, {"d": "d", "x": "x", "f": "t"}[kind])])
    nd = sum(1 for _, k in DOTFILES if k == "d")
    out.append([])
    out.append([(f"{nd} directories, {len(DOTFILES) - nd} files", "t")])
    return out


PLAN = [
    [("UCF Computer Science, May 2028", "t")],
    [("SWE Intern, Versant Media (Rotten Tomatoes)", "t")],
    [("backend systems + applied AI", "subtext0")],
    [("open to Summer 2027 SWE internships", "green")],
]


# Mobile: 36 columns, so every line is written to fit, never shrunk.
PLAN_M = [
    [("UCF Computer Science, May 2028", "t")],
    [("SWE Intern, Versant Media", "t")],
    [("on Rotten Tomatoes", "subtext0")],
    [("backend systems + applied AI", "subtext0")],
    [("open to Summer 2027 SWE intern", "green")],
]
WINS_M2 = [
    [("crisislens ", "blue"), ("Databricks 1st", "t")],
    [("           ", "t"), ("Hacklytics 2026", "subtext0")],
    [("farsight   ", "blue"), ("4 sponsor tracks", "t")],
    [("           ", "t"), ("Knight Hacks IX", "subtext0")],
    [("backrooms  ", "blue"), ("Hyphenate track prize", "t")],
    [("           ", "t"), ("Cal Hacks 13.0", "subtext0")],
]


def script(width, mobile):
    wins = WINS_MOB if mobile else WINS_DESK
    if mobile:
        return [
            ("~", "whoami", [[("azizu06", "t")]]),
            ("~", "cat .plan", PLAN_M),
            ("~", "cat wins.txt", WINS_M2),
            ("~", "ls ~/projects", ls_columns(LS_PROJECTS, width)),
        ]
    return [
        ("~", "whoami", [[("azizu06", "t")]]),
        ("~", "ls ~/projects", ls_columns(LS_PROJECTS, width)),
        ("~", "cat wins.txt", [[(n.ljust(11), "blue"), (w, "t")] for n, w in wins]),
        ("~", "gh pr list -R badges/shields -A @me -s merged", gh_lines(width)),
        ("~", "z dotfiles", []),
        ("dotfiles", "tree -L 1", tree_lines()),
    ]


def shell_pane(tl: Timeline, x0, y0, cw, lh, rows, width, start, mobile, t):
    """Returns SVG for the shell pane content (caller clips it)."""
    steps = script(width, mobile)
    lines = []  # (appear_time, tokens, row)
    typing = []  # (row, prompt_len, command, t_start, char_times)
    cursor = []  # (time, (col, row), visible)
    now = start
    row = 0
    rnd = 7
    for where, cmd, out in steps:
        p = prompt_tokens(where)
        plen = tlen(p)
        lines.append((now, p, row))
        cursor.append((now, (plen, row), 1))
        tc = now + 0.55
        seg_row, seg_col, seg_txt, seg_times = row, plen, "", []
        for i, ch in enumerate(cmd):
            rnd = (rnd * 1103515245 + 12345) & 0x7FFFFFFF
            tc += 0.045 + (rnd % 60) / 1000.0
            pos = plen + i
            r_i, c_i = row + pos // width, pos % width
            if r_i != seg_row:  # zsh soft-wraps a long command onto the next row
                typing.append((seg_row, seg_col, seg_txt, seg_times))
                seg_row, seg_col, seg_txt, seg_times = r_i, 0, "", []
                lines.append((tc, [], r_i))
            seg_txt += ch
            seg_times.append(tc)
            nxt = pos + 1
            cursor.append((tc, (nxt % width, row + nxt // width), 1))
        typing.append((seg_row, seg_col, seg_txt, seg_times))
        row = seg_row
        now = tc + 0.38
        row += 1
        cursor.append((now, (0, row), 0))
        for j, o in enumerate(out):
            assert tlen(o) <= width, (o, tlen(o), width)
            lines.append((now + j * 0.035, o, row))
            row += 1
        now += len(out) * 0.035 + (0.25 if not out else 2.3)
    # final prompt
    p = prompt_tokens(steps[-1][0])
    lines.append((now, p, row))
    cursor.append((now, (tlen(p), row), 1))
    end_t = now

    body = []
    for appear, toks, r in lines:
        y = y0 + r * lh + lh * 0.74
        body.append(tl.shown([(appear, tl.D)], tline(x0, y, cw, toks)))
    for i, (r, plen, cmd, ctimes) in enumerate(typing):
        y = y0 + r * lh + lh * 0.74
        cid = f"ty{'m' if mobile else 'd'}{i}"
        full = len(cmd) * cw + 2
        widths = [(ct, f(min((k + 1) * cw + 0.5, full))) for k, ct in enumerate(ctimes)]
        body.append(
            f'<clipPath id="{cid}"><rect x="{f(x0 + plen * cw)}" y="{f(y0 + r * lh)}" '
            f'width="{f(full)}" height="{lh}">{tl.discrete("width", widths, 0)}</rect></clipPath>'
            f'<g clip-path="url(#{cid})">{tline(x0, y, cw, [(cmd, "t")], plen)}</g>')
    # cursor: block, no blink (his Ghostty config), hidden while output prints
    pos = [(tm, (x0 + c * cw, y0 + r * lh + 1)) for tm, (c, r), _ in cursor]
    visp = [(tm, v) for tm, _, v in cursor]
    last_c, last_r = cursor[-1][1]
    base_tf = f"translate({f(x0 + last_c * cw)},{f(y0 + last_r * lh + 1)})"
    body.append(
        f'<g transform="{base_tf}">{tl.translate(pos, pos[0][1])}'
        f'<g opacity="1">{tl.discrete("opacity", visp, 0)}'
        + blink(f'<rect width="{f(cw)}" height="{lh - 2}" class="rosewater"/>') + "</g></g>")

    # scroll: when a row would fall off the bottom, shift up one row
    shifts = []
    for appear, _, r in lines:
        if r >= rows:
            shifts.append((appear, (0, -(r - rows + 1) * lh)))
    final_shift = shifts[-1][1] if shifts else (0, 0)
    inner = "".join(body)
    if shifts:
        inner = (f'<g transform="translate(0,{f(final_shift[1])})">'
                 f'{tl.translate(shifts, (0, 0))}{inner}</g>')
    return inner, end_t


# ---------------------------------------------------------------------------
# Neovim pane (desktop only)
# ---------------------------------------------------------------------------


def nvim_pane(tl: Timeline, x0, y0, cw, lh, rows, width_cols, pane_w, t, focus_end):
    """LazyVim: relative numbers, cursorline, global lualine, cmdline."""
    gutter = 5  # "  3  " style: number right-aligned in 3 cols, sign col
    tx = x0 + gutter * cw
    buf_rows = rows - 2
    for ln in BUFFER:
        assert gutter + tlen(ln) <= width_cols, (ln, gutter + tlen(ln))
    # cursor path: (time, row, col)
    states = [(0.0, 0, 0), (0.7, 1, 0), (1.05, 2, 2), (1.4, 3, 2), (1.75, 4, 2),
              (2.3, 4, 12), (3.0, 5, 2), (3.35, 6, 2)]
    t_colon, t_w, t_enter = 3.9, 4.2, 4.55
    out = []

    def row_y(r):
        return y0 + r * lh

    # state intervals
    ivals = []
    for i, (ts, r, c) in enumerate(states):
        te = states[i + 1][0] if i + 1 < len(states) else tl.D
        ivals.append((ts, te, r, c))
    static_t = 2.5  # static render: cursor on the role line

    for ts, te, r, c in ivals:
        g = [f'<rect x="{f(x0 - 6)}" y="{f(row_y(r))}" width="{f(pane_w)}" height="{lh}" class="cursorline"/>']
        for i in range(len(BUFFER)):
            if i == r:
                num, cls = str(i + 1), "lavender b"
                g.append(f'<text x="{f(x0 + 3 * cw)}" y="{f(row_y(i) + lh * 0.74)}" '
                         f'text-anchor="end" class="m {cls}">{num}</text>')
            else:
                num, cls = str(abs(i - r)), "surface1"
                g.append(f'<text x="{f(x0 + 3 * cw)}" y="{f(row_y(i) + lh * 0.74)}" '
                         f'text-anchor="end" class="m {cls}">{num}</text>')
        out.append(tl.shown([(ts, te)], "".join(g), static_t))

    for i, ln in enumerate(BUFFER):
        out.append(tline(tx, row_y(i) + lh * 0.74, cw, ln))

    # cursor block with the character under it drawn inverted
    for ts, te, r, c in ivals:
        line = "".join(x for x, _ in BUFFER[r]) if r < len(BUFFER) else ""
        ch = line[c] if c < len(line) else " "
        te2 = min(te, focus_end)
        if ts >= te2:
            continue
        cur = (f'<rect x="{f(tx + c * cw)}" y="{f(row_y(r) + 1)}" width="{f(cw)}" height="{lh - 2}" class="rosewater"/>')
        if ch.strip():
            cur += (f'<text x="{f(tx + c * cw)}" y="{f(row_y(r) + lh * 0.74)}" class="m base">{esc(ch)}</text>')
        out.append(tl.shown([(ts, te2)], blink(cur), static_t))

    # lualine (globalstatus)
    sy = row_y(buf_rows)
    sl_w = pane_w - 12
    sx = x0 - 6

    def seg_text(x, s, cls):
        return f'<text x="{f(x)}" y="{f(sy + lh * 0.74)}" class="m {cls}">{esc(s)}</text>'

    def arrow_r(x, cls):  # powerline  separator
        return f'<path d="M{f(x)} {f(sy)}L{f(x + 7)} {f(sy + lh / 2)}L{f(x)} {f(sy + lh)}Z" class="{cls}"/>'

    def arrow_l(x, cls):  # powerline  separator
        return f'<path d="M{f(x)} {f(sy)}L{f(x - 7)} {f(sy + lh / 2)}L{f(x)} {f(sy + lh)}Z" class="{cls}"/>'

    bar = [f'<rect x="{f(sx)}" y="{f(sy)}" width="{f(sl_w + 12)}" height="{lh}" class="mantle"/>']

    def mode_block(label, cls):
        w = (len(label) + 2) * cw
        return (f'<rect x="{f(sx)}" y="{f(sy)}" width="{f(w)}" height="{lh}" class="{cls}"/>'
                + seg_text(sx + cw, label, "mantle b") + arrow_r(sx + w, cls)), w

    nb, w_normal = mode_block("NORMAL", "blue")
    cb, w_cmd = mode_block("COMMAND", "peach")
    bar.append(tl.shown([(0, t_colon), (t_enter, tl.D)], nb, static_t))
    bar.append(tl.shown([(t_colon, t_enter)], cb, static_t))
    bx = sx + w_normal + 7
    bw = 7 * cw
    bar.append(f'<rect x="{f(bx)}" y="{f(sy)}" width="{f(bw)}" height="{lh}" class="surface0"/>'
               + seg_text(bx + cw, "main", "blue") + arrow_r(bx + bw, "surface0"))
    cx_ = bx + bw + 7 + cw
    bar.append(seg_text(cx_, BUFFER_NAME, "text b"))
    # right: progress + location (section y), clock (section z)
    zx = sx + sl_w + 12
    zw = 7 * cw
    bar.append(f'<rect x="{f(zx - zw)}" y="{f(sy)}" width="{f(zw)}" height="{lh}" class="blue"/>'
               + arrow_l(zx - zw, "blue"))
    bar.append(seg_text(zx - zw + 2 * cw, "lua", "mantle b"))
    yw = 7 * cw
    yx = zx - zw - 7 - yw
    bar.append(f'<rect x="{f(yx)}" y="{f(sy)}" width="{f(yw)}" height="{lh}" class="surface0"/>'
               + arrow_l(yx, "surface0"))
    for ts, te, r, c in ivals:
        bar.append(tl.shown([(ts, te)], seg_text(yx + cw, f"{r + 1:>2}:{c + 1:<2}", "blue"), static_t))
    out.append("".join(bar))

    # cmdline
    cy = row_y(buf_rows + 1) + lh * 0.74
    size = len(("\n".join("".join(x for x, _ in ln) for ln in BUFFER) + "\n").encode())
    msg = f'"{BUFFER_NAME}" {len(BUFFER)}L, {size}B written'
    out.append(tl.shown([(t_colon, t_w)], f'<text x="{f(sx + 2)}" y="{f(cy)}" class="m text">:</text>', static_t))
    out.append(tl.shown([(t_w, t_enter)], f'<text x="{f(sx + 2)}" y="{f(cy)}" class="m text">:w</text>', static_t))
    out.append(tl.shown([(t_enter, tl.D)], f'<text x="{f(sx + 2)}" y="{f(cy)}" class="m text">{esc(msg)}</text>', static_t))
    return "".join(out)


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------


def herdr_tabs(tl, x, y, w, cw, lh, active_pane_label=None):
    """herdr tab row: active tab number on blue, '+' for a new tab."""
    s = f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{lh}" class="mantle"/>'
    tw = 8 * cw
    s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(tw)}" height="{lh}" class="blue"/>'
    s += f'<text x="{f(x + tw / 2)}" y="{f(y + lh * 0.74)}" text-anchor="middle" class="m mantle">1</text>'
    s += f'<text x="{f(x + tw + 2.5 * cw)}" y="{f(y + lh * 0.74)}" class="m overlay1">+</text>'
    return s


def pane_box(x, y, w, h, cls, label=None, cw=7.5, lh=17, label_cls="overlay1"):
    s = f'<rect x="{f(x + 0.5)}" y="{f(y + 0.5)}" width="{f(w - 1)}" height="{f(h - 1)}" fill="none" stroke-width="1" class="{cls}" style="fill:none;stroke:currentColor"/>'
    return s


def box(x, y, w, h, color):
    return (f'<rect x="{f(x + 0.5)}" y="{f(y + 0.5)}" width="{f(w - 1)}" height="{f(h - 1)}" '
            f'fill="none" stroke="{color}" stroke-width="1"/>')


def digits_clock(x, y, cw, cls):
    """HH:MM:SS that really ticks: each digit position stacks its glyphs and
    shows one per slot, on its own SMIL loop (10 s, 60 s, 600 s)."""
    out = [f'<text x="{f(x)}" y="{f(y)}" class="m {cls}">21:4</text>']

    def digit(col, count, slot, start):
        parts = []
        dur = count * slot
        for i in range(count):
            d = (start + i) % count
            a, b = i * slot / dur, (i + 1) * slot / dur
            vals, kts = [], []
            if a > 0:
                vals.append(0); kts.append(0)
            vals.append(1); kts.append(a)
            if b < 1:
                vals.append(0); kts.append(b)
            kt = ";".join(f"{k:.4f}" for k in kts)
            base = 1 if i == 0 else 0
            parts.append(f'<text x="{f(x + col * cw)}" y="{f(y)}" class="m {cls}" opacity="{base}">'
                         f'<animate attributeName="opacity" dur="{dur:g}s" repeatCount="indefinite" '
                         f'calcMode="discrete" values="{";".join(map(str, vals))}" keyTimes="{kt}"/>{d}</text>')
        return "".join(parts)

    out.append(digit(4, 10, 60, 7))   # minute ones: 21:47 -> 21:48 ...
    out.append(f'<text x="{f(x + 5 * cw)}" y="{f(y)}" class="m {cls}">:</text>')
    out.append(digit(6, 6, 10, 0))    # seconds tens
    out.append(digit(7, 10, 1, 0))    # seconds ones
    return "".join(out)


def status_bar(tl, x, y, w, cw, lh, t, panes, focus_t, mobile):
    """tmux/herdr-style bar: session pill, pane list, live clock."""
    ty = y + lh * 0.74
    s = [f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{lh}" class="mantle"/>']
    sess = " aziz "
    sw = len(sess) * cw
    s.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(sw)}" height="{lh}" class="blue"/>')
    s.append(f'<text x="{f(x)}" y="{f(ty)}" class="m mantle b">{sess}</text>')
    px = x + sw + cw
    for i, name in enumerate(panes):
        label = f"{i + 1}:{name}"
        on = (0, focus_t) if i == 0 else (focus_t, tl.D)
        off = [(focus_t, tl.D)] if i == 0 else [(0, focus_t)]
        if len(panes) == 1:
            on, off = (0, tl.D), []
        lw_ = (len(label) + 2) * cw
        act = (f'<rect x="{f(px)}" y="{f(y)}" width="{f(lw_)}" height="{lh}" class="surface0"/>'
               f'<text x="{f(px + cw)}" y="{f(ty)}" class="m blue b">{esc(label)}*</text>')
        idle = f'<text x="{f(px + cw)}" y="{f(ty)}" class="m overlay1">{esc(label)}</text>'
        s.append(tl.shown([on], act))
        if off:
            s.append(tl.shown(off, idle))
        px += lw_
    right = "" if mobile else "azizu06 · ghostty"
    clock_w = 8 * cw
    cx = x + w - clock_w - cw
    s.append(f'<rect x="{f(cx - cw)}" y="{f(y)}" width="{f(clock_w + 2 * cw)}" height="{lh}" class="surface0"/>')
    s.append(digits_clock(cx, ty, cw, "text b"))
    s.append(f'<text x="{f(cx - 2 * cw)}" y="{f(ty)}" text-anchor="end" class="m overlay1">{esc(right)}</text>')
    return "".join(s)


def border_label(x, y, label, cw, cls, t):
    w = (len(label) + 2) * cw
    return (f'<rect x="{f(x + 8)}" y="{f(y - 1)}" width="{f(w)}" height="3" class="base"/>'
            f'<text x="{f(x + 8 + cw)}" y="{f(y + 4)}" class="m {cls} b">{esc(label)}</text>')


def hero(t, mobile):
    if mobile:
        W, size, lh = 380, 17, 23
    else:
        W, size, lh = 860, 15, 21
    cw = size * 0.6
    title_h = 34 if mobile else 30
    padx, pady = 10, 8
    rows = 20 if not mobile else 19
    pane_y = title_h + pady + 4
    pane_h = rows * lh + 12
    bar_y = pane_y + pane_h + 6
    H = int(bar_y + lh + pady)
    inner_w = W - 2 * padx

    focus_switch = 0 if mobile else 5.2
    D = 46.0 if not mobile else 26.0
    tl = Timeline(D)
    body = [f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" class="base" '
            f'stroke="{t["frame"]}" stroke-width="1"/>']
    body.append(traffic_lights(18, title_h / 2))
    title = "herdr: aziz" if mobile else "herdr: aziz — nvim aziz.lua"
    body.append(f'<text x="{W / 2}" y="{title_h / 2 + (5 if mobile else 4)}" text-anchor="middle" class="s subtext0" '
                f'font-size="{15 if mobile else 12.5}" font-weight="600">{esc(title)}</text>')

    if mobile:
        px, pw = padx, inner_w
        cols = int((pw - 14) // cw)
        clip = f'<clipPath id="shm"><rect x="{px + 1}" y="{pane_y + 7}" width="{pw - 2}" height="{rows * lh}"/></clipPath>'
        sh, end_t = shell_pane(tl, px + 7, pane_y + 7, cw, lh, rows, cols, 0.6, True, t)
        body.append(clip + f'<g clip-path="url(#shm)">{sh}</g>')
        body.append(box(px, pane_y, pw, pane_h, t["blue"]))
        body.append(border_label(px, pane_y, "zsh", cw, "blue", t))
        body.append(status_bar(tl, padx, bar_y, inner_w, cw, lh, t, ["zsh"], 0, True))
    else:
        gap = 6
        need = 5 + max(tlen(ln) for ln in BUFFER)
        lw = round(need * cw + 14)
        rw = inner_w - gap - lw
        lx, rx = padx, padx + lw + gap
        lcols = int((lw - 14) // cw)
        rcols = int((rw - 14) // cw)
        nv = nvim_pane(tl, lx + 7, pane_y + 7, cw, lh, rows, lcols, lw - 2, t, focus_switch)
        body.append(f'<clipPath id="nvc"><rect x="{lx + 1}" y="{pane_y + 1}" width="{f(lw - 2)}" height="{pane_h - 2}"/></clipPath>')
        body.append(f'<g clip-path="url(#nvc)">{nv}</g>')
        sh, end_t = shell_pane(tl, rx + 7, pane_y + 7, cw, lh, rows, rcols, focus_switch + 0.4, False, t)
        body.append(f'<clipPath id="shd"><rect x="{f(rx + 1)}" y="{pane_y + 7}" width="{f(rw - 2)}" height="{rows * lh}"/></clipPath>')
        body.append(f'<g clip-path="url(#shd)">{sh}</g>')
        # pane borders + labels: the focused pane is blue (herdr), the other overlay0
        for (bx, bw, name), active in (((lx, lw, "nvim"), (0, focus_switch)), ((rx, rw, "zsh"), (focus_switch, D))):
            idle = [(0, active[0])] if active[0] > 0 else [(active[1], D)]
            body.append(tl.shown([active], box(bx, pane_y, bw, pane_h, t["blue"])
                                 + border_label(bx, pane_y, name, cw, "blue", t)))
            body.append(tl.shown(idle, box(bx, pane_y, bw, pane_h, t["overlay0"])
                                 + border_label(bx, pane_y, name, cw, "overlay1", t)))
        body.append(status_bar(tl, padx, bar_y, inner_w, cw, lh, t, ["nvim", "zsh"], focus_switch, False))
    assert end_t < D - 2.5, (end_t, D)
    alt = ("A Ghostty terminal running herdr with Catppuccin Mocha. Left pane: Neovim "
           "editing aziz.lua, a profile written as a Lua table: Abduaziz Umarov, UCF "
           "Computer Science May 2028, SWE Intern at Versant Media on Rotten Tomatoes, "
           "builds backend systems and applied AI, open to Summer 2027 SWE internships. "
           "Right pane: a zsh session types ls ~/projects, cat wins.txt (CrisisLens 1st "
           "in the Databricks Challenge at Hacklytics 2026, Farsight 4 sponsor tracks at "
           "Knight Hacks IX, Backrooms Hyphenate track prize at Cal Hacks 13.0), gh pr list "
           "for 3 merged badges/shields PRs, and tree of the dotfiles repo.")
    if mobile:
        alt = ("A Ghostty terminal running herdr with Catppuccin Mocha. A zsh session types "
               "whoami, cat .plan (UCF Computer Science May 2028, SWE Intern at Versant Media "
               "on Rotten Tomatoes, backend systems and applied AI, open to Summer 2027 SWE "
               "internships), cat wins.txt (CrisisLens 1st in the Databricks Challenge at "
               "Hacklytics 2026, Farsight 4 sponsor tracks at Knight Hacks IX, Backrooms "
               "Hyphenate track prize at Cal Hacks 13.0), and ls ~/projects.")
    return svg_doc(W, H, t, size, "".join(body), alt), alt


# ---------------------------------------------------------------------------
# Project cards: herdr panes with the label on the border
# ---------------------------------------------------------------------------


def wrap(s, width):
    words, lines, cur = s.split(), [], ""
    for w in words:
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= width:
            cur += " " + w
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def card(t, p, mobile):
    W = 380 if mobile else 860
    size = 16 if mobile else 13
    lh = 23 if mobile else 19
    cw = size * 0.6
    pad = 14
    cols = int((W - 2 * pad) // cw)
    win = p["win_m"] if mobile else p["win"]
    desc = wrap(p["desc"], cols)
    top = 12 if mobile else 10
    y = top + (20 if mobile else 18)
    body = []
    repo = p["repo"] if len(p["repo"]) + 2 <= cols else p["repo"].replace("github.com/", "")
    # break the award line at " · " so a venue name never splits
    win_lines, cur = [], ""
    for part in win.split(" · "):
        trial = part if not cur else cur + " · " + part
        if len(trial) <= cols or not cur:
            cur = trial
        else:
            win_lines.append(cur)
            cur = part
    win_lines.append(cur)
    rows = [[(w_, "peach")] for w_ in win_lines] + [[(d, "subtext1")] for d in desc] + [[("→ ", "overlay1"), (repo, "blue")]]
    H = int(y + len(rows) * lh + 6)
    label = f" {p['dir']} "
    lw = len(label) * cw
    gx0, gx1 = pad - 4, pad - 4 + lw + 8
    yb = top + 0.5
    body.append(f'<rect x="1" y="{top}" width="{W - 2}" height="{H - top - 1}" class="base"/>')
    body.append(f'<path d="M{f(gx0)} {f(yb)}H1.5V{f(H - 0.5)}H{f(W - 1.5)}V{f(yb)}H{f(gx1)}" '
                f'fill="none" stroke="{t["overlay0"]}" stroke-width="1"/>')
    # herdr-style label sitting in a gap of the top border
    body.append(f'<text x="{f(pad)}" y="{f(top + size * 0.35)}" class="m blue b">{esc(label)}</text>')
    for i, r in enumerate(rows):
        body.append(tline(pad, y + i * lh + lh * 0.7, cw, r))
    alt = f"{p['dir']}: {win}. {p['desc']} {p['repo']}"
    return svg_doc(W, H, t, size, "".join(body), alt), alt


def small_link(t, label, mobile=False):
    size = 16 if mobile else 11.5
    cw = size * 0.6
    w = int((len(label) + 4) * cw + 8) + (16 if mobile else 0)
    h = 40 if mobile else 22
    ty = h / 2 + size * 0.35
    x0 = 16 if mobile else 8
    body = (box(0, 0, w, h, t["overlay0"])
            + f'<text x="{f(x0)}" y="{f(ty)}" class="m overlay1">↗</text>'
            + f'<text x="{f(x0 + 2 * cw)}" y="{f(ty)}" class="m blue">{esc(label)}</text>')
    return svg_doc(w, h, t, size, body, label), w


def tab_button(t, idx, label, mobile=False):
    size = 16 if mobile else 13
    cw = size * 0.6
    num_w = 4 * cw
    # mobile: fixed 150 px so two sit per row, 44 px tall for a thumb
    w = 150 if mobile else int(num_w + (len(label) + 2) * cw)
    h = 44 if mobile else 24
    ty = h / 2 + size * 0.35
    body = (f'<rect x="0" y="0" width="{w}" height="{h}" class="mantle"/>'
            f'<rect x="0" y="0" width="{f(num_w)}" height="{h}" class="blue"/>'
            f'<text x="{f(num_w / 2)}" y="{f(ty)}" text-anchor="middle" class="m mantle b">{idx}</text>'
            f'<text x="{f(num_w + cw)}" y="{f(ty)}" class="m text">{esc(label)}</text>')
    return svg_doc(w, h, t, size, body, label), w


# ---------------------------------------------------------------------------
# README assembly
# ---------------------------------------------------------------------------

VARIANTS = [("dark", "dark", False), ("light", "light", False), ("m-dark", "dark", True), ("m-light", "light", True)]


def write(rel, content):
    path = ASSETS / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def picture(name, alt, width="100%", has_mobile=True):
    """width=None leaves the size to the chosen SVG, so desktop and mobile
    sources can have different intrinsic sizes."""
    src = []
    if has_mobile:
        src.append(f'<source media="(max-width: 760px) and (prefers-color-scheme: dark)" srcset="assets/m-dark/{name}.svg">')
        src.append(f'<source media="(max-width: 760px)" srcset="assets/m-light/{name}.svg">')
    src.append(f'<source media="(prefers-color-scheme: dark)" srcset="assets/dark/{name}.svg">')
    w = f' width="{width}"' if width else ""
    return f'<picture>{"".join(src)}<img src="assets/light/{name}.svg" alt="{esc(alt)}"{w}></picture>'


def main():
    alts = {}
    for folder, theme, mobile in VARIANTS:
        t = THEMES[theme]
        svg, alt = hero(t, mobile)
        write(f"{folder}/hero.svg", svg)
        if not mobile:
            alts["hero"] = alt
        for p in PROJECTS:
            svg, alt = card(t, p, mobile)
            write(f"{folder}/{p['slug']}.svg", svg)
            if not mobile:
                alts[p["slug"]] = alt
        for p in PROJECTS:
            if p["extra"]:
                svg, w = small_link(t, p["extra"][0], mobile)
                write(f"{folder}/link-{p['slug']}.svg", svg)
                alts[f"link-{p['slug']}"] = f"{p['dir']}: {p['extra'][0]}"
        for i, (label, url, alt) in enumerate(LINKS, 1):
            svg, w = tab_button(t, i, label, mobile)
            write(f"{folder}/tab-{i}.svg", svg)
            alts[f"tab-{i}"] = alt

    md = ["<!-- Generated by scripts/build_readme.py. Edit the script, not this file. -->", ""]
    md.append(f'<p><a href="https://azizu.dev">{picture("hero", alts["hero"])}</a></p>')
    md.append("")
    for p in PROJECTS:
        line = f'<p><a href="{p["url"]}">{picture(p["slug"], alts[p["slug"]])}</a>'
        if p["extra"]:
            line += (f'<br><a href="{p["extra"][1]}">'
                     f'{picture("link-" + p["slug"], alts["link-" + p["slug"]], None)}</a>')
        md.append(line + "</p>")
        md.append("")
    tabs = []
    for i, (label, url, _) in enumerate(LINKS, 1):
        tabs.append(f'<a href="{url}">{picture(f"tab-{i}", alts[f"tab-{i}"], None)}</a>')
    md.append('<p align="center">\n' + "\n".join(tabs) + "\n</p>")
    (ROOT / "README.md").write_text("\n".join(md) + "\n")
    print("wrote README.md and", sum(1 for _ in ASSETS.rglob("*.svg")), "svgs")


if __name__ == "__main__":
    main()
