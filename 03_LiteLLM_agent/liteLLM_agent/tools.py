def analyzer_code(code:str,language:str)-> dict:
    """
    Analyze source code and return basic information
    about the supplied code.

    Args: 
         code : Source code to analyze.
         language:Programming language.

    Return:
         Dictionary containing code analysis information.

    """
    return {
        "language":language,
        "line":len(code.splitlines()),
        "characters":len(code),
    }