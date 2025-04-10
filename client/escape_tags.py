# %%
# escape non-valid html tags

import re
import html

# A fairly comprehensive set of standard HTML5 tags:
VALID_HTML5_TAGS = {
    # Main root/document sections
    "html",
    "head",
    "body",
    # Document metadata
    "title",
    "base",
    "link",
    "meta",
    "style",
    # Content sectioning
    "address",
    "article",
    "aside",
    "footer",
    "header",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "main",
    "nav",
    "section",
    # Text content
    "blockquote",
    "dd",
    "dir",
    "div",
    "dl",
    "dt",
    "figcaption",
    "figure",
    "hr",
    "li",
    "ol",
    "p",
    "pre",
    "ul",
    # Inline text semantics
    "a",
    "abbr",
    "b",
    "bdi",
    "bdo",
    "br",
    "cite",
    "code",
    "data",
    "dfn",
    "em",
    "i",
    "kbd",
    "mark",
    "q",
    "rb",
    "rp",
    "rt",
    "rtc",
    "ruby",
    "s",
    "samp",
    "small",
    "span",
    "strong",
    "sub",
    "sup",
    "time",
    "u",
    "var",
    "wbr",
    # Image and multimedia
    "area",
    "audio",
    "img",
    "map",
    "track",
    "video",
    "picture",
    "source",
    # Embedded content
    "embed",
    "iframe",
    "object",
    "param",
    "video",
    # SVG / MathML could be included, but that is more complex to handle
    # Scripting
    "canvas",
    "noscript",
    "script",
    # Demarcating edits
    "del",
    "ins",
    # Table content
    "caption",
    "col",
    "colgroup",
    "table",
    "tbody",
    "td",
    "tfoot",
    "th",
    "thead",
    "tr",
    # Forms
    "button",
    "datalist",
    "fieldset",
    "form",
    "input",
    "label",
    "legend",
    "meter",
    "optgroup",
    "option",
    "output",
    "progress",
    "select",
    "textarea",
    # Interactive elements
    "details",
    "dialog",
    "menu",
    "menuitem",
    "summary",
    # Web Components & misc new tags
    "template",
    "slot",
    # Others (deprecated or less common)
    "applet",
    "acronym",
    "big",
    "center",
    "font",
    "strike",
    "tt",
    "basefont",
    "marquee",  # etc., up to your preference
}

# Regex to match something that looks like an HTML tag:
# We'll capture the entire "<...>" structure in group 1.
tag_pattern = re.compile(r"(<[^>]*>)")


def is_valid_html_tag(tag_str: str) -> bool:
    """
    Checks if `tag_str` is a syntactically valid HTML tag
    and its tag name is in VALID_HTML5_TAGS (opening, closing, or self-closing).
    """
    # Remove outer angle brackets: "<" and ">"
    inner = tag_str[1:-1].strip()
    if not inner:
        return False

    # If it's a closing tag: </tag>
    if inner.startswith("/"):
        # e.g. </div>
        tag_name = inner[1:].strip().lower()

        # Make sure there's no extra space/attributes after the name
        if " " in tag_name:
            return False

        return tag_name in VALID_HTML5_TAGS

    # If it's opening or self-closing, e.g.: <div>, <div class="foo">, <img ... />
    # Let's split on whitespace to separate the tag name from attributes if any
    parts = inner.split(None, 1)
    # The first part might be "div", "img", or "img/" (self-closing syntax).
    if not parts:
        return False

    first_part = parts[0].lower()

    # If the tag might be self-closing, it could end with "/"
    # e.g. <img src="..." /> => the first part might be "img", or it might be "img/"
    if first_part.endswith("/"):
        first_part = first_part[:-1].strip()

    # Now, the `first_part` should be the bare tag name if it's valid
    if not re.match(r"^[a-zA-Z0-9]+$", first_part):
        # Maybe there's an attribute jammed right after the name, e.g. "divclass" => invalid
        # or something else. We'll attempt a more robust check:
        match_name = re.match(r"^([a-zA-Z0-9]+)", first_part)
        if not match_name:
            return False
        first_part = match_name.group(1).lower()

    # Finally, check if the tag name is recognized in our set
    return first_part in VALID_HTML5_TAGS


def escape_nonvalid_html_tags(text: str) -> str:
    """
    Finds all substrings that look like HTML tags and escapes them
    unless they appear to be valid HTML5 tags.
    """

    def replace_tag(m: re.Match) -> str:
        raw_tag = m.group(1)
        if is_valid_html_tag(raw_tag):
            return raw_tag
        else:
            print('escaping', raw_tag)
            return html.escape(raw_tag)

    return tag_pattern.sub(replace_tag, text)


# %%
import json

domains = ["krasota", "travel_creation", "synonims_list", "samopoznanie", "pretrain_hf"]
for domain in domains:
    filename = f"./test_data/gemba_4_{domain}.json"
    texts = json.load(open(filename, "r", encoding="utf8"))

    texts = [escape_nonvalid_html_tags(x) for x in texts]

    json.dump(
        texts,
        open(filename.replace(".json", "_escaped.json"), "w", encoding="utf8"),
        ensure_ascii=False,
        indent=4,
    )


# # filename = "./test_data/gemba_sft_27.1.json"
# filename = "./test_data/gemba_4_redactor.json"

# texts = json.load(open(filename, "r", encoding="utf8"))

# print(len(texts))

# texts[0]

# # %%
# texts = [escape_nonvalid_html_tags(x) for x in texts]

# # %%
# json.dump(
#     texts,
#     open(filename.replace(".json", "_escaped.json"), "w", encoding="utf8"),
#     ensure_ascii=False,
# )

# # %%

# %%
import json

filename = f"./test_data/gemba_5_all_domains.json"
texts = json.load(open(filename, "r", encoding="utf8"))

texts = [escape_nonvalid_html_tags(x) for x in texts]

json.dump(
    texts,
    open(filename.replace(".json", "_escaped.json"), "w", encoding="utf8"),
    ensure_ascii=False,
    indent=4,
)
# %%
