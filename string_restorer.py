
import sys

target_file = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    
    # Simple state machine to detect unclosed quotes
    # ignoring comments and escapes for now (should be rare in these print strings)
    
    def get_unclosed_quote(s):
        in_q = None # ' or "
        in_f = False
        escaped = False
        for char in s:
            if char == '\\':
                escaped = not escaped
                continue
            if escaped:
                escaped = False
                continue
            if char in ("'", '"'):
                if in_q == char:
                    in_q = None
                elif in_q is None:
                    # Ignore quotes in comments
                    # Wait, if we are mid-string, # is just a character.
                    # This is complex. Let's simplify:
                    in_q = char
            elif char == '#' and in_q is None:
                return None # Comment starts, no unclosed quote before it
        return in_q

    unclosed = get_unclosed_quote(line)
    if unclosed:
        # Join with next line(s)
        j = i + 1
        while j < len(lines):
            next_line = lines[j].strip()
            line = line.rstrip() + " " + next_line + "\n"
            if get_unclosed_quote(line) is None:
                j += 1
                break
            j += 1
        new_lines.append(line)
        i = j
    else:
        new_lines.append(line)
        i += 1

with open(target_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Universal string restorer complete.")
