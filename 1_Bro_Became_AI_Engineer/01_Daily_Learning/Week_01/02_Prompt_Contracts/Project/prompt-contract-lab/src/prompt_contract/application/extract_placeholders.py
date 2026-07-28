import re


def extract_placeholders(template: str) -> set[str]:
    """
    Extract placeholder names from a template.

    Example:
        "Hello {name}, welcome to {company}"
        -> {"name", "company"}
    """
    return set(re.findall(r"{(.*?)}", template))