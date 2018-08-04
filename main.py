from Portfolio_Wrapper import CronScript
import datetime


def main():
    script_bot = CronScript('localhost')
    try:
        script_bot.run_updates()
        print('Update successful at {}'.format(datetime.datetime.now()))
    except Exception:
        print('Update failed, review log for details')


if __name__ == '__main__':
    main()
