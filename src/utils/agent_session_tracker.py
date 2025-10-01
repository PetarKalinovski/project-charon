from rich.panel import Panel
from rich import print as rprint
from rich.padding import Padding


class AgentSessionTracker:
    def __init__(self):
        self.active_session = None
        self.session_style = None

    def start_session(self, agent_name: str, query: str, style_config: dict):
        """Start a new agent session"""
        self.active_session = agent_name
        self.session_style = style_config

        # Print session header
        rprint(
            Padding(
                Panel(
                    f"[bold {style_config['color']}]🔄 {style_config['emoji']} {style_config['name']} Session Started[/bold {style_config['color']}]\n"
                    f"[dim]Query: {query}[/dim]",
                    border_style=style_config["color"],
                    title=f"{style_config['emoji']} Agent Working",
                ),
                pad=style_config["padding"],
            )
        )

    def session_print(self, content: str, is_main_response: bool = False):
        """Print content within the current session styling"""
        if not self.active_session:
            rprint(content)
            return

        style = self.session_style

        if is_main_response:
            rprint(
                Padding(
                    Panel(
                        f"[{style['color']}]{style['emoji']} {style['name']}:[/{style['color']}] {content}",
                        border_style=style["color"],
                        title=f"{style['emoji']} Response",
                    ),
                    pad=style["padding"],
                )
            )
        else:
            rprint(
                Padding(
                    f"[{style['color']}]│[/{style['color']}] {content}",
                    pad=(0, 0, 0, style["padding"][3] + 2),
                )
            )

    def end_session(self):
        """End the current session"""
        if self.active_session and self.session_style:
            style = self.session_style
            rprint(
                Padding(
                    f"[{style['color']}]└─ {style['name']} completed[/{style['color']}]",
                    pad=(0, 0, 0, style["padding"][3] + 2),
                )
            )
        self.active_session = None
        self.session_style = None
