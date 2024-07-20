import re

def extract_python_code(input_string, language = 'python'):
    """
    Extracts Python code enclosed in triple backticks from a given string.

    Parameters:
    input_string (str): The string containing the Python code.

    Returns:
    str: The extracted Python code, or a message indicating no code was found.
    """
    code_pattern = r"```" + language + r"\n(.*?)```"
    matches = re.findall(code_pattern, input_string, re.DOTALL)
    return matches if matches else []

def replace_single_backslashes(json_string):
    """
    Replaces single backslashes (\\) with double backslashes (\\\\) in a given JSON string,
    while leaving already double backslashes untouched.
    """
    placeholder = "DOUBLEBACKSLASH"
    temp_string = json_string.replace('\\\\', placeholder)
    temp_string = temp_string.replace('\\', '\\\\')
    final_string = temp_string.replace(placeholder, '\\\\')
    return final_string

def split_latex_with_keys(text):
    pattern = r'(\$\$.*?\$\$)|(\$.*?\$)|' + \
              r'(\\\[[^\]]*?\\\])|(\\\([^\)]*?\\\))|' + \
              r'(\\begin\{.*?\}.*?\\end\{.*?\})'
    def determine_latex_type(part):
        if len(part) <= 15 and (part.startswith('$') or part.startswith('\\(')):
            return 'Latex1'
        else:
            return 'Latex2'
    latex_parts = re.findall(pattern, text, flags=re.DOTALL)
    latex_parts = [item for sublist in latex_parts for item in sublist if item]
    result = []
    last_index = 0
    for part in latex_parts:
        index = text.find(part, last_index)
        if index > last_index:
            result.append({'Type': 'Text', 'Content': text[last_index:index]})
        part_type = determine_latex_type(part)
        result.append({'Type': part_type, 'Content': part})
        last_index = index + len(part)
    if last_index < len(text):
        result.append({'Type': 'Text', 'Content': text[last_index:]})
    return result


def extract_text_with_complete_sentences(input_string):
    """
    Extracts text from a LaTeX-formatted string. It captures the title after \section{},
    the text within single quotes in list items, and complete sentences following an \item.
    
    Args:
    input_string (str): A string formatted in LaTeX, containing sections, subsections, and items.
    
    Returns:
    list: A list of extracted strings.
    """
    pattern = r"\\section\{([^}]*)\}|\\item '([^']*)'|\\item ([^'\n].*?[\.\?\!])"
    matches = re.findall(pattern, input_string)
    extracted_texts = [''.join(match).strip() for match in matches if ''.join(match).strip()]
    return extracted_texts

def extract_moduler(latex_text):
    # This pattern now includes a broader match for items, including those with LaTeX commands
    pattern = r"\\item[^:]*:\s*'([^']*)'|\\item[^:]*:\s*([^\n]*)"
    matches = re.findall(pattern, latex_text)

    # Extract and clean up the matches
    cleaned_matches = [match[0] if match[0] else match[1].strip() for match in matches]
    return cleaned_matches

# Test cases
example_texts = [
    "Here is an equation $a^2 + b^2 = c^2$ which is well-known.",
    "Aligned equations: \\begin{align} a &= b \\\\ c &= d \\end{align} End of example.",
    "Inline math: \\( e^{i\\pi} + 1 = 0 \\) is Euler's identity. $ 1+ 1  = 2$. btw\n",
    "Displayed math: \\[ \\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi} \\].",
    "Here is an equation $$a^2 + b^2 = c^2$$ which has two dollar-signs.",
    "hey \\begin{gather}x=2+3-5\\cdot7\\rightarrow9<10≥11≤12>13\\end{gather} you",
    "\\begin{gather}y=(a+b)\\cdot(c-d)\\rightarrow(e+f)\\end{gather}",
    "z=[(x+y)\\cdot{a-b}\\rightarrow{c+d}]",
    "$a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z$",
    "x^{2}+y^{2}=z^{2}",
    "hallå eller $a_{1}+b_{2}\\cdot c_{3}-d_{4}\\leq e_{5}+f_{6}$ ja du",
    "$a+(b+c\\cdot{d-e}\\rightarrow f)$",
    "\(a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z\)"
]



if __name__ == '__main__':
    processed_texts = [split_latex_with_keys(text) for text in example_texts]
    print(processed_texts)