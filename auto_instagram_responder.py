from instagrapi import Client
import schedule
import time


from instagrapi import Client
import schedule
import time

# Initialize the client
cl = Client()
username = ""
password = ""
# Step 1: Login with Two-Factor Authentication Handling
try:
    cl.login("pereproxima", "Alphacentuari090#")
except Exception as e:
    if "Two-factor authentication required" in str(e):
        verification_code = input("Enter the verification code sent to your phone/email: ")
        cl.login("pereproxima", "Alphacentuari090#", verification_code=verification_code)

# Keep track of messages already responded to
responded_messages = set()

def auto_responder():
    # Step 2: Fetch all threads
    threads = cl.direct_threads()

    if threads:
        for thread in threads:
            # Fetch messages for the thread
            messages = cl.direct_messages(thread.id)

            for msg in messages:
                # Skip already responded messages
                if msg.id in responded_messages:
                    continue

                # Check message content and respond
                if "hi" in msg.text.lower() or "hello" in msg.text.lower():
                    cl.direct_send("Hello! How can I assist you?", thread.id)
                elif "info" in msg.text.lower():
                    cl.direct_send("Here's some information about our services...", thread.id)

                # Add the message ID to the responded set
                responded_messages.add(msg.id)
    else:
        print('No threads available.')

# Step 3: Schedule the auto-responder to run every minute
schedule.every(1).minute.do(auto_responder)

# Step 4: Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
