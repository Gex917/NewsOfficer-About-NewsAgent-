"""
任务调度器 - 定时执行新闻收集
"""

import threading
from datetime import datetime
from typing import Callable, List

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.cron import CronTrigger
    HAS_APSCHEDULER = True
except ImportError:
    HAS_APSCHEDULER = False


class TaskScheduler:
    """任务调度器"""

    def __init__(self):
        self.scheduler = None
        self.jobs = []
        self.is_running = False
        self._manual_callbacks = []

        if HAS_APSCHEDULER:
            self.scheduler = BackgroundScheduler()

    def add_scheduled_task(self, time_str: str, callback: Callable, task_name: str = "news_collect"):
        """
        添加定时任务

        Args:
            time_str: 时间字符串，格式 "HH:MM"
            callback: 回调函数
            task_name: 任务名称
        """
        if not HAS_APSCHEDULER:
            print("[!] apscheduler 未安装，定时任务不可用")
            print("[!] 请运行: pip install apscheduler")
            return

        hour, minute = time_str.split(":")
        trigger = CronTrigger(hour=int(hour), minute=int(minute))

        job = self.scheduler.add_job(
            callback,
            trigger=trigger,
            id=f"{task_name}_{time_str.replace(':', '')}",
            name=f"{task_name} at {time_str}",
            replace_existing=True
        )
        self.jobs.append(job)
        print(f"[✓] 已添加定时任务: {task_name} @ {time_str}")

    def add_manual_callback(self, callback: Callable):
        """添加手动触发回调"""
        self._manual_callbacks.append(callback)

    def start(self):
        """启动调度器"""
        if self.scheduler and not self.is_running:
            self.scheduler.start()
            self.is_running = True
            print("[✓] 调度器已启动")
            self._print_jobs()

    def stop(self):
        """停止调度器"""
        if self.scheduler and self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            print("[✓] 调度器已停止")

    def trigger_now(self):
        """立即执行一次任务"""
        print("[*] 手动触发任务...")
        for callback in self._manual_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"[!] 任务执行失败: {e}")

    def _print_jobs(self):
        """打印所有任务"""
        if not self.jobs:
            print("[*] 暂无定时任务")
            return

        print("\n" + "=" * 40)
        print("已注册的定时任务:")
        print("=" * 40)
        for job in self.jobs:
            print(f"  • {job.name} (下次执行: {job.next_run_time})")
        print("=" * 40 + "\n")

    def get_next_run_time(self) -> str:
        """获取下次执行时间"""
        if not self.jobs:
            return "无定时任务"

        next_times = []
        for job in self.jobs:
            if job.next_run_time:
                next_times.append(job.next_run_time)

        if not next_times:
            return "无定时任务"

        next_time = min(next_times)
        return next_time.strftime("%Y-%m-%d %H:%M:%S")


class SimpleScheduler:
    """简单调度器（不依赖 apscheduler）"""

    def __init__(self):
        self.tasks = []
        self.is_running = False
        self._thread = None

    def add_task(self, hour: int, minute: int, callback: Callable):
        """添加任务"""
        self.tasks.append((hour, minute, callback))

    def start(self):
        """启动调度器"""
        self.is_running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        print("[✓] 简单调度器已启动")

    def stop(self):
        """停止调度器"""
        self.is_running = False

    def _run(self):
        """运行循环"""
        import time
        executed_today = set()

        while self.is_running:
            now = datetime.now()
            current_time = (now.hour, now.minute)

            for hour, minute, callback in self.tasks:
                task_key = f"{hour}:{minute}"

                if current_time == (hour, minute) and task_key not in executed_today:
                    try:
                        callback()
                        executed_today.add(task_key)
                    except Exception as e:
                        print(f"[!] 任务执行失败: {e}")

            # 午夜重置
            if now.hour == 0 and now.minute == 0:
                executed_today.clear()

            time.sleep(30)  # 每30秒检查一次
