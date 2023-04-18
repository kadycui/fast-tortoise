from tortoise import Tortoise, run_async
from email_validator import validate_email, EmailNotValidError
from common.logger import logger
from common.database import db_config
from models.user import User
from utils.hash import get_hash_password



class CreateSuperUser:
    """
    初始化管理员账号
    """

    @staticmethod
    async def create_superuser():
        print('开始创建管理员用户')
        print('请输入用户名:')
        username = input()
        print('请输入密码:')
        password = input()
        print('请输入邮箱:')
        success_email = None
        while True:
            email = input()
            try:
                success_email = validate_email(email).email
            except EmailNotValidError:
                print('邮箱不符合规范，请重新输入：')
                continue
            break
        await User.create(
            username=username,
            password=get_hash_password(password),
            email=success_email,
            is_superuser=True,
            creator='init'
        )
        logger.success(f'管理员用户创建成功, 账号:{username}, 密码:{password}')

    async def init_data(self):
        """
        初始化集
        """
        logger.info('*************** 初始化数据库连接 ***************')
        await Tortoise.init(config=db_config)
        logger.success('*************** 连接数据库成功 ***************')

        logger.info('*************** 开始初始化数据 ***************')
        await self.create_superuser()
        logger.info('*************** 数据初始化完成 ***************')


if __name__ == '__main__':
    create_superuser = CreateSuperUser()
    run_async(create_superuser.init_data())