import click


def echo(k, v):
    click.echo(click.style(f"{k}: ".title(), fg='green', bold=True) + v)


def echo_dictionary(dictionary, depth=0, indent=4 * " "):
    for k, v in sorted(dictionary.items()):
        if isinstance(v, dict):
            echo(depth * indent + k.replace("_", " ").title(), "")
            echo_dictionary(v, depth=depth + 1)
        elif isinstance(v, list):
            echo(depth * indent + k.replace("_", " ").title(), "")
            for i, item in enumerate(v):
                echo((depth + 1) * indent + f"{i:02d}", "")
                echo_dictionary(item, depth=depth + 2)
        elif isinstance(v, set):
            echo(depth * indent + k.replace("_", " ").title(), "")
            for i, item in enumerate(sorted(v)):
                echo((depth + 1) * indent + f"{i:02d}", "")
                echo_dictionary(item, depth=depth + 2)
        else:
            echo(depth * indent + k.replace("_", " ").title(), str(v))
