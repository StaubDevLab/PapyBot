import re


def regex(extract):
    intro = re.search(r"(?P<intro>[^=]*)", extract).group('intro')
    results = re.findall(r"[=]+(?P<titre>[^=]*)[=]+(?P<content>[^==]*)", extract)
    results.insert(0, ('Informations Générales', intro))
    return results


def layout(extract):
    result = list()
    regex_list = regex(extract)
    for elt in regex_list:
        elt = list(elt)
        elt[0] = f"<li><strong>{elt[0]}: </strong></li>"
        result.append(elt[0])
        result.append(elt[1])
    return " ".join(result)
