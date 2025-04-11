# ------------ imports ------------
import os

# ------------ setup ------------
os.system("")


# ------------ class setup ------------
class HealthBar:
    symbol_remaining: str = "█"
    symbol_lost: str = "_"
    barrier: str = "|"
    colors: dict = {"red": "\033[91m",
                    "purple": "\33[95m",
                    "blue": "\33[34m",
                    "blue2": "\33[36m",
                    "blue3": "\33[96m",
                    "green": "\033[92m",
                    "green2": "\033[32m",
                    "brown": "\33[33m",
                    "yellow": "\33[93m",
                    "grey": "\33[37m",
                    "default": "\033[0m",
                    # Bold colors
                    "bold_red": "\033[91;1m",
                    "bold_green": "\033[92;1m",
                    "bold_yellow": "\033[93;1m",
                    "bold_blue": "\033[94;1m",
                    "bold_magenta": "\033[95;1m",
                    "bold_cyan": "\033[96;1m",
                    "bold_white": "\033[97;1m"
                    }

    def __init__(self,
                 entity,
                 length: int = 20,
                 is_colored: bool = True,
                 color: str = "") -> None:
        self.entity = entity
        self.length = length
        self.max_value = entity.health_max
        self.current_value = entity.health

        self.is_colored = is_colored
        self.color = self.colors.get(color) or self.colors["default"]
        
        # For visual health state
        self.previous_value = self.current_value
        self.animation_frames = 0
        
        # Status effect indicators
        self.status_symbols = {
            "poison": "☠",
            "burn": "🔥",
            "freeze": "❄"
        }

    def update(self) -> None:
        self.previous_value = self.current_value
        self.current_value = self.entity.health
        self.animation_frames = 5  # Show animation for 5 frames

    def draw(self) -> None:
        # Calculate health bar segments
        remaining_bars = round(self.current_value / self.max_value * self.length)
        lost_bars = self.length - remaining_bars
        
        # Determine health color based on percentage
        health_percent = self.current_value / self.max_value
        bar_color = self.color
        
        if health_percent <= 0.25:
            bar_color = self.colors["red"]
        elif health_percent <= 0.5:
            bar_color = self.colors["yellow"]
        
        # Show damage animation if health decreased recently
        damage_indicator = ""
        if self.animation_frames > 0:
            if self.current_value < self.previous_value:
                damage = self.previous_value - self.current_value
                damage_indicator = f" \033[91m(-{damage})\033[0m"
            elif self.current_value > self.previous_value:
                heal = self.current_value - self.previous_value
                damage_indicator = f" \033[92m(+{heal})\033[0m"
            self.animation_frames -= 1
        
        # Add status effect indicators
        status_indicators = ""
        if hasattr(self.entity, 'status_effects'):
            for status, data in self.entity.status_effects.items():
                if status in self.status_symbols:
                    status_color = "31" if status == "burn" else "32" if status == "poison" else "36"  # Red for burn, green for poison, cyan for freeze
                    status_indicators += f" \033[{status_color}m{self.status_symbols[status]}\033[0m"
        
        # Add level indicator if entity has level
        level_indicator = ""
        if hasattr(self.entity, 'level'):
            level_indicator = f" [Lvl {self.entity.level}]"
        
        # Print the health bar
        print(f"{self.entity.name}{level_indicator}'s HEALTH: {self.entity.health}/{self.entity.health_max}{damage_indicator}{status_indicators}")
        print(f"{self.barrier}"
              f"{bar_color if self.is_colored else ''}"
              f"{remaining_bars * self.symbol_remaining}"
              f"{lost_bars * self.symbol_lost}"
              f"{self.colors['default'] if self.is_colored else ''}"
              f"{self.barrier}")
        
    def draw_boss_health(self) -> None:
        """Special health bar display for boss enemies"""
        if not hasattr(self.entity, 'phase'):
            self.draw()
            return
            
        # Calculate health bar segments
        remaining_bars = round(self.current_value / self.max_value * self.length)
        lost_bars = self.length - remaining_bars
        
        # Boss health bars have phase indicators
        phase_markers = ""
        for threshold in self.entity.phase_thresholds:
            marker_position = round((1 - threshold) * self.length)
            phase_markers += f"\033[33m|\033[0m" + " " * (marker_position - 1)
        
        # Print boss header
        print(f"\033[95;1m==== BOSS: {self.entity.name} [Phase {self.entity.phase}] ====\033[0m")
        print(f"HEALTH: {self.entity.health}/{self.entity.health_max}")
        
        # Print the health bar
        print(f"{self.barrier}"
              f"{self.color if self.is_colored else ''}"
              f"{remaining_bars * self.symbol_remaining}"
              f"{lost_bars * self.symbol_lost}"
              f"{self.colors['default'] if self.is_colored else ''}"
              f"{self.barrier}")
