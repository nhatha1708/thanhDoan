from thanhDoan.thanhDoan import ThanhDoan
import schedule
import time 

def run_bot():
    try:
        with ThanhDoan() as bot:
            bot.land_first_page()
            data = bot.get_data()
            new_df = bot.new_df(data)
            bot.to_csv(new_df)
    except Exception as e:
        print(e)
        print("There is a problem running this program from the command line interface")

schedule.every().day.at("00:00").do(run_bot)

while True:
    print("Waiting for")
    time.sleep(1300)
    schedule.run_pending()
    