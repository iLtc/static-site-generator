def markdown_to_blocks(markdown: str) -> list[str]:
    results = []

    for line in markdown.split("\n\n"):
        line = line.strip()

        if not line:
            continue

        results.append(line)

    return results
