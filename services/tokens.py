from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs

from aiogram.client.session import aiohttp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy.ext.asyncio import AsyncSession

from config import APPLICATION, EMAIL, CLIENT_SECRET
from config import CLIENT_ID, REDIRECT_URI
from repositories.tokens import TokenRepository


class TokenService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add_tokens(self, user_id: int, data: dict):
        token = TokenRepository(self.session)
        await token.add_token(
            user_id=user_id,
            data=data,
        )
    
    async def check_token(self, user_id: int):
        token_time = TokenRepository(self.session)
        result = await token_time.get_token_time(user_id)
        if result is not None and ((datetime.now() - result) > timedelta(days=13)):
            await self.refresh_token()
    
    async def get_token(self, user_id: int):
        token = TokenRepository(self.session)
        return await token.get_token(user_id)
    
    async def get_refresh_token(self, user_id: int):
        token = TokenRepository(self.session)
        return await token.get_refresh_token(user_id)
    
    async def refresh_token(self, user_id: int):
        url = "https://oauth.vk.com/token"
        headers = {
            "Authorization": f"Bearer {await self.get_token(user_id)}",
            "User-Agent": f"{APPLICATION} ({EMAIL})",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": await self.get_refresh_token(user_id),
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, headers=headers, data=data) as resp:
                new_token = await resp.json()
                await TokenRepository(self.session).update_token(
                    user_id=user_id,
                    data=new_token,
                )
    
    async def create_tokens(self, user_id: int):
        auth_code = get_code()
        url = "https://api.hh.ru/token"
        headers = {
            "User-Agent": APPLICATION,
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, headers=headers, data=data) as resp:
                data = await resp.json()
                await TokenRepository(self.session).add_token(
                    user_id=user_id,
                    data=data,
                )


def get_code():
    phone = input("Введите телефон, привязанный к hh.ru: ")
    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(options=options)
        
        auth_url = (f"https://hh.ru/oauth/authorize?response_type=code&client_id={CLIENT_ID}"
                    f"&redirect_uri={REDIRECT_URI}")
        driver.get(auth_url)
        
        phone_input = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, "input[data-qa='login-input-username']")
            )
        )
        phone_input.send_keys(phone)
        driver.find_element(
            By.CSS_SELECTOR, "button[data-qa='account-login-submit']"
        ).click()
        
        WebDriverWait(driver, 30).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, "input[data-qa='otp-code-input']")
            )
        )
        
        WebDriverWait(driver, 60).until(lambda d: REDIRECT_URI in d.current_url)
        final_url = driver.current_url
        if "code=" in final_url:
            code = parse_qs(urlparse(final_url).query)["code"][0]
            return code
        return None
    
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        if driver and "code=" in driver.current_url:
            code = parse_qs(urlparse(driver.current_url).query)["code"][0]
            return code
        return None
    finally:
        if driver:
            driver.quit()
