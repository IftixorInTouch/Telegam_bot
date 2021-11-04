from typing import Union

import asyncpg
from asyncpg.pool import Pool


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(
            user="postgres",
            password="LmntrxWS1",
            host="localhost",
            database="telegram"
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False):
        result = None
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """CREATE TABLE IF NOT EXISTS Users(
        id BIGSERIAL PRIMARY KEY,
        username VARCHAR (255),
        user_id BIGINT NOT NULL UNIQUE,
        parent_name VARCHAR (255),
        parent_id BIGINT,
        referals INTEGER DEFAULT 0,
        bonus NUMERIC (9, 2) DEFAULT 0 
        );
        """
        await self.execute(sql, execute=True)

    async def add_user(self, username, user_id):
        sql = """INSERT INTO Users (username, user_id) VALUES($1, $2) returning *"""
        return await self.execute(sql, username, user_id, execute=True)

    async def add_parent(self, username, user_id, parent_name, parent_id, referals, bonus):
        sql = """
        INSERT INTO Users (username, user_id, parent_name, parent_id, referals, bonus)
        VALUES ($1, $2, $3, $4, $5, $6) returning *
        """
        return await self.execute(sql, username, user_id, parent_name, parent_id, referals, bonus, execute=True)

    async def select_user(self, user_id):
        sql = f"""SELECT * FROM Users WHERE user_id={user_id}"""
        return await self.execute(sql, fetch=True)

    async def select_users(self):
        sql = """SELECT * FROM users"""
        return await self.execute(sql, fetch=True)

    async def select_username(self, user_id):
        sql = f"""SELECT username FROM users WHERE user_id={user_id}"""
        return await self.execute(sql, fetchval=True)

    async def drop_user(self, user_id):
        sql = f"""DELETE FROM Users WHERE user_id={user_id}"""
        return await self.execute(sql, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def sum_bonuses(self, parent_id):
        sql = f"""SELECT SUM(bonus) FROM Users WHERE parent_id={parent_id}"""
        return await self.execute(sql, fetchrow=True)

    async def add_referer(self, parent_id):
        sql = """INSERT INTO bonuses (user_id) VALUES ($1) returning *"""
        return await self.execute(sql, parent_id, execute=True)

    async def add_bonus(self, parent_id):
        quantity = await self.sum_bonuses(parent_id)
        sql = f"""UPDATE bonuses SET bonus = {quantity[0]} WHERE user_id = $1"""
        return await self.execute(sql, parent_id, execute=True)

    async def select_referer(self, parent_id):
        sql = """SELECT * FROM bonuses WHERE user_id = $1"""
        return await self.execute(sql, parent_id, fetch=True)

    async def select_bonus(self, user_id):
        sql = """SELECT bonus FROM bonuses WHERE user_id = $1"""
        return await self.execute(sql, user_id, fetchval=True)
