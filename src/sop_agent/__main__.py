"""CLI entry point for sop-agent.

Commands:
    sop-agent onboard               Interactive setup of a new overlay
    sop-agent new <description>     Generate a new SOP
    sop-agent validate <path>       Validate an existing SOP file
    sop-agent list                  List available pillars and service lines
    sop-agent overlay               Show the currently resolved overlay
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from sop_agent import __version__
from sop_agent.overlay import OverlayNotFoundError, resolve_overlay

app = typer.Typer(
    name="sop-agent",
    help="Author high-quality SOPs sized to how your team actually operates.",
    no_args_is_help=True,
    add_completion=False,
)

console = Console()


@app.command()
def version() -> None:
    """Print the installed version."""
    console.print(f"sop-agent {__version__}")


@app.command()
def overlay(
    overlay_path: Annotated[
        Path | None,
        typer.Option("--overlay", help="Path to your overlay directory."),
    ] = None,
) -> None:
    """Show the currently resolved overlay (where governance + org-map come from)."""
    try:
        config = resolve_overlay(overlay_path)
    except OverlayNotFoundError as err:
        console.print(f"[red]Overlay not found:[/red] {err}")
        raise typer.Exit(code=1) from err

    table = Table(title="Overlay resolution")
    table.add_column("Field")
    table.add_column("Value")
    table.add_row("Source", config.source)
    table.add_row("Path", str(config.path) if config.path else "(none — using bundled examples)")
    table.add_row(
        "Governance dir",
        str(config.governance_dir) if config.governance_dir else "(not present)",
    )
    table.add_row(
        "Org-map dir",
        str(config.org_map_dir) if config.org_map_dir else "(not present)",
    )
    console.print(table)


@app.command()
def onboard(
    overlay_path: Annotated[
        Path | None,
        typer.Option("--overlay", help="Where to write the new overlay."),
    ] = None,
) -> None:
    """Interactive setup: walk through the questions and write a starter overlay."""
    console.print(
        Panel.fit(
            "[bold]Onboarding[/bold]\n\n"
            "This command will be wired to the Onboarding subagent in Phase 1.\n"
            "Today it's a stub. Coming soon:\n\n"
            "  1. Detect your org's archetype (Lean / Coordinated / Compliance-Forward)\n"
            "  2. Capture services, tools, and brand voice\n"
            "  3. Build a starter [cyan]roles.yaml[/cyan]\n"
            "  4. Write everything to your overlay path\n",
            title="sop-agent onboard",
            border_style="cyan",
        )
    )


@app.command()
def new(
    description: Annotated[str, typer.Argument(help="What the SOP should cover.")],
    overlay_path: Annotated[
        Path | None,
        typer.Option("--overlay", help="Path to your overlay directory."),
    ] = None,
) -> None:
    """Generate a new SOP from a natural-language description."""
    try:
        config = resolve_overlay(overlay_path)
    except OverlayNotFoundError as err:
        console.print(f"[red]Overlay not found:[/red] {err}")
        raise typer.Exit(code=1) from err

    console.print(
        Panel.fit(
            f"[bold]Generate SOP[/bold] (Phase 1 — stub)\n\n"
            f"  Description: {description}\n"
            f"  Overlay:     {config.path or '(fallback to bundled examples)'}\n"
            f"  Source:      {config.source}\n\n"
            f"The Conductor agent will be wired here in Phase 1.\n",
            title="sop-agent new",
            border_style="cyan",
        )
    )


@app.command()
def validate(
    sop_path: Annotated[Path, typer.Argument(help="Path to a .sop.md or generated SOP file.")],
) -> None:
    """Validate an SOP file against the framework's format rules."""
    if not sop_path.exists():
        console.print(f"[red]File not found:[/red] {sop_path}")
        raise typer.Exit(code=1)

    console.print(
        Panel.fit(
            f"[bold]Validate SOP[/bold] (Phase 1 — stub)\n\n"
            f"  File: {sop_path}\n\n"
            f"Validation rules will be wired in Phase 1.\n",
            title="sop-agent validate",
            border_style="cyan",
        )
    )


@app.command(name="list")
def list_pillars() -> None:
    """List available pillars and service lines."""
    pillars = {
        "strategy": ["marketing-strategy", "marketing-analytics"],
        "branding": ["branding-creative-services", "content-studio"],
        "website": ["conversion-rate-optimization", "web-design-development"],
        "acquisition": [
            "paid-media",
            "seo",
            "social-media-management",
            "content-marketing",
            "cold-email",
        ],
        "retention": ["email-marketing", "sms-marketing"],
        "agentic-ai": [
            "ai-audit-fit",
            "ready-built-ai-systems",
            "enterprise-agentic-ai",
            "automation",
            "agents-for-small-business",
        ],
    }

    table = Table(title="Pillars and service lines")
    table.add_column("Pillar", style="cyan")
    table.add_column("Service lines")
    for pillar, services in pillars.items():
        table.add_row(pillar, "\n".join(services))
    console.print(table)


if __name__ == "__main__":
    app()
