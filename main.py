from thanhDoan.thanhDoan import ThanhDoan
import schedule
import time 

try:
    with ThanhDoan() as bot:
        bot.land_first_page()
        data = bot.get_data()
        bot.to_csv(data)
except Exception as e:
    print(f"An error occurred: {str(e)}")

# def run_bot():
#     try:
#         with ThanhDoan() as bot:
#             bot.land_first_page()
#             data = bot.get_data()
#             bot.to_csv(data)
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         print("There is a problem running this program from the command line interface")


# schedule.every().day.at("00:00").do(run_bot)

# while True:
#     print("Waiting for scheduled time...")
#     schedule.run_pending()
#     time.sleep(60)
    