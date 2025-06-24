# Print iterations progress.
# Adapted from https://stackoverflow.com/a/34325723.
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

# Progress bar with color.
def printProgressBarColor (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    fill_prefix = '\33[31m'
    fill_suffix = '\033[0m'
    prog = iteration/total
    if(prog > 0.33 and prog <= 0.67): fill_prefix = '\33[33m'
    elif(prog > 0.67): fill_prefix = '\33[32m'
    fill = fill_prefix + fill + fill_suffix
    printProgressBar(iteration, total, prefix = prefix, suffix = suffix, decimals = decimals, length = length, fill = fill, printEnd = printEnd)
    return

def printProgressWithOutput(progress, total, recent_lines, prefix='', suffix='',
                           max_lines=5, width=80, decimals=1, length=100, fill='█'):
    """
    Print progress bar followed by bordered scrolling output in one operation
    """
    # Calculate progress bar
    percent = ("{0:." + str(decimals) + "f}").format(100 * (progress / float(total)))
    filledLength = int(length * progress // total)
    bar = fill * filledLength + '-' * (length - filledLength)

    # Build the complete display
    lines_to_show = list(recent_lines)[-max_lines:] if recent_lines else []

    # Calculate the total width of the progress bar for alignment
    progress_bar_text = f'{prefix} |{bar}| {percent}% {suffix}'
    progress_bar_width = len(progress_bar_text)

    # Use the wider of the two for consistency
    box_width = max(width, progress_bar_width)
    content_width = box_width - 4  # Account for "| " and " |"

    # Clear the area we're going to write to
    total_lines = 1 + max_lines + 2  # progress bar + border + output lines + border
    # if(progress == 0.): total_lines = max_lines + 1

    print("\033[{}A\033[2K".format(total_lines), end='')  # Move up and clear line

    # Print progress bar
    print(f'{progress_bar_text:<{box_width}}')

    # Print top border
    print("\033[2K", end='')
    print("┌{}┐".format('─' * (box_width - 2)))

    # Print output lines with border
    for i in range(max_lines):
        print("\033[2K", end='')  # Clear line
        if i < len(lines_to_show):
            line = lines_to_show[i]
            display_line = line.rstrip('\n\r')
            if len(display_line) > content_width:
                display_line = display_line[:content_width-3] + "..."
            print(f"│ {display_line:<{content_width}} │") # TODO: Maybe find equivalent using format()? Might improve Python2 compatibility
        else:
            print("│{}│".format(' ' * (box_width - 2)))  # Empty line with border

    # Print bottom border
    print("\033[2K", end='')
    print(f"└{'─' * (box_width - 2)}┘")