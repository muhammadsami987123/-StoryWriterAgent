"""
StoryWriterAgent - Main Entry Point
Day 36 of #100DaysOfAI-Agents
Author: Muhammad Sami
"""
import argparse
import sys
from colorama import init, Fore, Style

init()  # Initialize colorama for Windows

from config import Config, EXAMPLE_PROMPTS
from story_agent import StoryAgent


def print_banner():
    """Print the application banner"""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   {Fore.YELLOW}StoryWriterAgent{Fore.CYAN} - AI Creative Writing Assistant      ║
║   Day 36 of #100DaysOfAI-Agents                          ║
║   Author: Muhammad Sami                                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


def print_help():
    """Print help information"""
    help_text = f"""
{Fore.GREEN}Available Commands:{Style.RESET_ALL}
  generate <prompt>  - Generate a new story interactively
  list              - Display all saved stories
  search <query>    - Search stories by content
  favorites         - Show favorite stories
  stats             - Display writing statistics
  examples          - Show example prompts
  config            - View current settings
  help              - Show this help message
  exit/quit         - Exit the application

{Fore.GREEN}Keyboard Shortcuts:{Style.RESET_ALL}
  Ctrl+C            - Cancel current operation
"""
    print(help_text)


def interactive_generate(agent: StoryAgent):
    """Interactive story generation"""
    print(f"\n{Fore.YELLOW}=== Story Generation ==={Style.RESET_ALL}\n")

    # Get prompt
    prompt = input(f"{Fore.CYAN}Enter your story idea: {Style.RESET_ALL}").strip()
    if not prompt:
        print(f"{Fore.RED}Error: Please provide a story idea.{Style.RESET_ALL}")
        return

    # Genre selection
    print(f"\n{Fore.GREEN}Available Genres:{Style.RESET_ALL}")
    for i, genre in enumerate(Config.GENRES, 1):
        print(f"  {i}. {genre}")
    genre_choice = input(f"{Fore.CYAN}Select genre (1-{len(Config.GENRES)}) [1]: {Style.RESET_ALL}").strip()
    genre = Config.GENRES[int(genre_choice) - 1] if genre_choice.isdigit() and 1 <= int(genre_choice) <= len(Config.GENRES) else Config.GENRES[0]

    # Tone selection
    print(f"\n{Fore.GREEN}Available Tones:{Style.RESET_ALL}")
    for i, tone in enumerate(Config.TONES, 1):
        print(f"  {i}. {tone}")
    tone_choice = input(f"{Fore.CYAN}Select tone (1-{len(Config.TONES)}) [1]: {Style.RESET_ALL}").strip()
    tone = Config.TONES[int(tone_choice) - 1] if tone_choice.isdigit() and 1 <= int(tone_choice) <= len(Config.TONES) else Config.TONES[0]

    # Length selection
    print(f"\n{Fore.GREEN}Available Lengths:{Style.RESET_ALL}")
    lengths = list(Config.LENGTHS.keys())
    for i, length in enumerate(lengths, 1):
        print(f"  {i}. {Config.LENGTHS[length]['label']}")
    length_choice = input(f"{Fore.CYAN}Select length (1-{len(lengths)}) [2]: {Style.RESET_ALL}").strip()
    length = lengths[int(length_choice) - 1] if length_choice.isdigit() and 1 <= int(length_choice) <= len(lengths) else "medium"

    # Language selection
    print(f"\n{Fore.GREEN}Available Languages:{Style.RESET_ALL}")
    for i, lang in enumerate(Config.LANGUAGES, 1):
        print(f"  {i}. {lang}")
    lang_choice = input(f"{Fore.CYAN}Select language (1-{len(Config.LANGUAGES)}) [1]: {Style.RESET_ALL}").strip()
    language = Config.LANGUAGES[int(lang_choice) - 1] if lang_choice.isdigit() and 1 <= int(lang_choice) <= len(Config.LANGUAGES) else Config.LANGUAGES[0]

    print(f"\n{Fore.YELLOW}Generating your {genre} story with {tone} tone in {language}...{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}\n")

    # Generate with streaming
    for chunk in agent.generate_story_stream(prompt, genre, tone, length, language):
        print(chunk, end="", flush=True)

    print(f"\n\n{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}Story saved successfully!{Style.RESET_ALL}\n")


def list_stories(agent: StoryAgent):
    """List all stories"""
    stories = agent.get_all_stories()
    if not stories:
        print(f"\n{Fore.YELLOW}No stories found. Generate your first story!{Style.RESET_ALL}\n")
        return

    print(f"\n{Fore.YELLOW}=== Your Stories ({len(stories)} total) ==={Style.RESET_ALL}\n")
    for story in stories:
        fav = "★" if story.get('favorite') else "☆"
        print(f"  {Fore.CYAN}{fav}{Style.RESET_ALL} [{story['id'][:8]}] {story['genre']} | {story['tone']} | {story['word_count']} words")
        print(f"    {Fore.WHITE}Prompt: {story['prompt'][:50]}...{Style.RESET_ALL}")
        print()


def search_stories(agent: StoryAgent, query: str):
    """Search stories"""
    results = agent.search_stories(query)
    if not results:
        print(f"\n{Fore.YELLOW}No stories found matching '{query}'{Style.RESET_ALL}\n")
        return

    print(f"\n{Fore.YELLOW}=== Search Results ({len(results)} found) ==={Style.RESET_ALL}\n")
    for story in results:
        fav = "★" if story.get('favorite') else "☆"
        print(f"  {Fore.CYAN}{fav}{Style.RESET_ALL} [{story['id'][:8]}] {story['genre']} | {story['prompt'][:40]}...")
    print()


def show_favorites(agent: StoryAgent):
    """Show favorite stories"""
    favorites = agent.get_favorites()
    if not favorites:
        print(f"\n{Fore.YELLOW}No favorite stories yet.{Style.RESET_ALL}\n")
        return

    print(f"\n{Fore.YELLOW}=== Favorite Stories ({len(favorites)}) ==={Style.RESET_ALL}\n")
    for story in favorites:
        print(f"  {Fore.YELLOW}★{Style.RESET_ALL} [{story['id'][:8]}] {story['genre']} | {story['prompt'][:40]}...")
    print()


def show_stats(agent: StoryAgent):
    """Show writing statistics"""
    stats = agent.get_stats()
    print(f"\n{Fore.YELLOW}=== Writing Statistics ==={Style.RESET_ALL}\n")
    print(f"  Total Stories: {Fore.CYAN}{stats['total_stories']}{Style.RESET_ALL}")
    print(f"  Total Words: {Fore.CYAN}{stats['total_words']}{Style.RESET_ALL}")
    print(f"  Average Words/Story: {Fore.CYAN}{stats['average_words']}{Style.RESET_ALL}")
    print(f"  Favorites: {Fore.YELLOW}{stats['favorites']}{Style.RESET_ALL}")

    if stats['genres']:
        print(f"\n  {Fore.GREEN}Genres:{Style.RESET_ALL}")
        for genre, count in stats['genres'].items():
            print(f"    {genre}: {count}")

    if stats['tones']:
        print(f"\n  {Fore.GREEN}Tones:{Style.RESET_ALL}")
        for tone, count in stats['tones'].items():
            print(f"    {tone}: {count}")
    print()


def show_examples():
    """Show example prompts"""
    print(f"\n{Fore.YELLOW}=== Example Prompts ==={Style.RESET_ALL}\n")
    for i, example in enumerate(EXAMPLE_PROMPTS, 1):
        print(f"  {i}. {example}")
    print()


def show_config():
    """Show current configuration"""
    print(f"\n{Fore.YELLOW}=== Configuration ==={Style.RESET_ALL}\n")
    print(f"  Model: {Fore.CYAN}{Config.OPENAI_MODEL}{Style.RESET_ALL}")
    print(f"  Host: {Fore.CYAN}{Config.HOST}{Style.RESET_ALL}")
    print(f"  Port: {Fore.CYAN}{Config.PORT}{Style.RESET_ALL}")
    print(f"  Stories Dir: {Fore.CYAN}{Config.STORIES_DIR}{Style.RESET_ALL}")
    print()


def quick_generate(agent: StoryAgent, prompt: str, genre: str, tone: str, length: str, language: str):
    """Quick story generation"""
    print(f"\n{Fore.YELLOW}Generating story...{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}\n")

    for chunk in agent.generate_story_stream(prompt, genre, tone, length, language):
        print(chunk, end="", flush=True)

    print(f"\n\n{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}Story saved successfully!{Style.RESET_ALL}\n")


def terminal_mode():
    """Run in terminal/interactive mode"""
    print_banner()
    print_help()

    try:
        agent = StoryAgent()
        print(f"{Fore.GREEN}Agent initialized successfully!{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"{Fore.RED}Error initializing agent: {e}{Style.RESET_ALL}")
        sys.exit(1)

    while True:
        try:
            command = input(f"{Fore.CYAN}StoryWriter> {Style.RESET_ALL}").strip().lower()

            if not command:
                continue
            elif command in ['exit', 'quit', 'q']:
                print(f"\n{Fore.YELLOW}Goodbye! Happy writing!{Style.RESET_ALL}\n")
                break
            elif command == 'help':
                print_help()
            elif command.startswith('generate'):
                interactive_generate(agent)
            elif command == 'list':
                list_stories(agent)
            elif command.startswith('search '):
                query = command[7:].strip()
                search_stories(agent, query)
            elif command == 'favorites':
                show_favorites(agent)
            elif command == 'stats':
                show_stats(agent)
            elif command == 'examples':
                show_examples()
            elif command == 'config':
                show_config()
            else:
                print(f"{Fore.RED}Unknown command. Type 'help' for available commands.{Style.RESET_ALL}")

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Operation cancelled.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="StoryWriterAgent - AI Creative Writing Assistant"
    )
    parser.add_argument('--web', action='store_true', help='Start web interface')
    parser.add_argument('--terminal', action='store_true', help='Start terminal interface')
    parser.add_argument('--quick', type=str, help='Quick story generation with prompt')
    parser.add_argument('--genre', type=str, default='Fantasy', help='Story genre')
    parser.add_argument('--tone', type=str, default='Serious', help='Story tone')
    parser.add_argument('--length', type=str, default='medium', help='Story length (short/medium/long)')
    parser.add_argument('--language', type=str, default='English', help='Story language')

    args = parser.parse_args()

    if args.web:
        from web_app import run_server
        run_server()
    elif args.quick:
        print_banner()
        agent = StoryAgent()
        quick_generate(agent, args.quick, args.genre, args.tone, args.length, args.language)
    else:
        terminal_mode()


if __name__ == "__main__":
    main()
