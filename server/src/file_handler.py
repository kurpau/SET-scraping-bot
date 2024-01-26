import os

def write_to_file(name, ticker, eps_list, url):
    file_path = os.path.join(os.getcwd(), "result.txt")
    with open(file_path, "a") as f:
        f.write(f"{name} [ {ticker} ] \n")
        f.write(f'|{"-" * 21}|\n')
        f.write(f"| {'Current':<8} | {'Previous':<8} | \n")
        f.write(f'|{"-" * 21}|\n')
        f.write(f"| {eps_list[0]:>8} | {eps_list[1]:>8} | \n")
        f.write(f'|{"-" * 21}|\n')
        f.write(f"Link to F45 page: {url}\n\n")
