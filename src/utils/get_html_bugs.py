from html.parser import HTMLParser


class UnclosedTagParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.open_tags = []
        self.unclosed_details = {}
        self.total_tags = 0

    def handle_starttag(self, tag, attrs):
        if tag not in ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track',
                       'wbr']:
            self.total_tags += 1
            self.open_tags.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        for open_tag in self.open_tags:
            if open_tag[0] == tag:
                self.open_tags.remove(open_tag)
                break

    def get_unclosed_tags(self):
        unclosed_tags = [pos for _, pos in self.open_tags]
        ratio = len(unclosed_tags) / self.total_tags if self.total_tags > 0 else 0
        return 1 - ratio, unclosed_tags


def find_repeated_css_styles(html):
    css_styles = {}
    total_css_rules = 0
    start = html.find('<style>')

    while start != -1:
        end = html.find('</style>', start)
        if end != -1:
            css_content = html[start + 7:end]
            style_start_line = html[:start].count('\n') + 1
            for rule in css_content.split('}'):
                if rule.strip():
                    css_name = rule.split('{')[0].strip()
                    if "@media" in css_name:
                        continue
                    line_number = style_start_line + css_content[:css_content.index(rule)].count('\n')

                    # Ensure the rule only gets counted once per line number
                    if css_name not in css_styles:
                        css_styles[css_name] = set([line_number])
                    else:
                        css_styles[css_name].add(line_number)

            total_css_rules += len([rule for rule in css_content.split('}') if rule.strip()])
        start = html.find('<style>', end)

    repeated_css = {k: v for k, v in css_styles.items() if len(v) > 1}
    ratio = len(repeated_css) / total_css_rules if total_css_rules > 0 else 0

    repeated_css_details = []
    for _, lines in repeated_css.items():
        repeated_css_details.extend(list(lines))  # Use list to ensure a proper flattening

    repeated_css_details = list(set(repeated_css_details))

    return 1 - ratio, repeated_css_details


def count_html_bugs(html):
    unclosed_parser = UnclosedTagParser()
    unclosed_parser.feed(html)
    unclosed_tags_ratio, unclosed_tags_details = unclosed_parser.get_unclosed_tags()

    repeated_css_ratio, repeated_css_details = find_repeated_css_styles(html)

    response = {
        "global_score": unclosed_tags_ratio * 0.7 + repeated_css_ratio * 0.3,
        "unclosed_tags": unclosed_tags_details,
        "repeated_css": repeated_css_details
    }

    print(response)
    return response
