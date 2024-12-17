import requests

# 假设 FastAPI 应用运行在 localhost:9031
BASE_URL = "http://localhost:9013/auth/register"

def test_register(username, password):
    print("Response text:", response.text)
    response = requests.post(BASE_URL, json={"username": username, "password": password})
    if response.status_code == 200:
        print("Registration successful:", response.json())
    elif response.status_code == 400:
        print("Registration failed:", response.json())
    else:
        print("Error:", response.json())

if __name__ == "__main__":
    # 测试用例
    test_cases = [
        {"username": "lrl001", "password": "123"},  # 新用户
        {"username": "", "password": "password123"},             # 用户名为空
        {"username": "new_user_2", "password": ""},              # 密码为空
        {"username": "lvrulan", "password": "lvrulan123"},   # 重复用户名
    ]

    for case in test_cases:
        print(f"Testing registration for {case['username']}...")
        test_register(case["username"], case["password"])