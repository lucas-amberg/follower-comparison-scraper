from bs4 import BeautifulSoup
import selenium.webdriver as webdriver

def get_desired_accounts():
    keep_going = True
    desired_accounts = set()
    while keep_going:
        print('Please enter an Instagram username to add to the comparison')
        desired_accounts.add(input('> ').lower())
        if (input('Would you like to add another account? [Y/N]\n> ').lower() != "y"):
            keep_going = False
    return desired_accounts

def scrape_accounts(desired_accounts):
    follower_counts = {}
    for account in desired_accounts:
        url = f'https://www.instagram.com/{account}'
        driver = webdriver.Chrome()
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        if (soup.title.text == 'Page not found • Instagram'):
            print(f'Please only input valid accounts...')
            print(f'@{account} is not a valid Instagram account')
            return -1
        else:
            follower_counts[account] = scrape_account(soup)
    result = sort_accounts(follower_counts)
    for i, item in enumerate(result):
        print(f'{i}: @{item[0]} - {item[1]} Followers')

def sort_accounts(follower_counts):
    return sorted(follower_counts.items(), key=lambda x:x[1], reverse=True)

def scrape_account(soup):
    description = soup.find('meta', property='og:description')['content']
    return description.split(' ')[0].replace(',',"")


if __name__ == '__main__':
    desired_accounts = get_desired_accounts()
    scrape_accounts(desired_accounts)
    