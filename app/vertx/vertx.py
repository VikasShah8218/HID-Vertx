import socket
import threading
import time

VRTX_IP = "192.168.1.252"
HOST_IP = "192.168.1.199"
VRTX_PORT = 4050
HOST_PORT = 4070

exit_event = threading.Event()

def event_server(controller_connection):
    event_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    event_socket.bind((HOST_IP, HOST_PORT))
    event_socket.listen(5)
    print(f"Event server listening on port {HOST_PORT}")

    while not exit_event.is_set():
        client_socket, addr = event_socket.accept()
        print(f"V1000 connected from {addr}")

        # Store the connection
        controller_connection[addr[0]] = client_socket
        initialize_connection(addr[0], controller_connection)
        try:
            while not exit_event.is_set():
                event_data = client_socket.recv(1024)
                if not event_data:
                    break
                event_handler(event_data.decode('utf-8'))
        except Exception as e:
            print(f"Event error: {e}")
        finally:
            client_socket.close()
            controller_connection[addr] = None

# Function to send messages to the controller using the stored connection
def send_message(message, controller_connection=None, addr=None):
    if controller_connection is None:
        controller_connection = {}

    if addr and addr in controller_connection:
        conn = controller_connection[addr]
        if conn:
            try:
                conn.send(message)
                print(f"Sent: {message}")
            except Exception as e:
                print(f"Error sending message: {e}")
    else:
        print("No active connection to send message.")


def accept_connection(addr=None, controller_connection=None):
    """Send accept connection command"""
    send_message(b"0070;0010;", controller_connection, addr)

def contact_controller(addr=None, controller_connection=None):
    """Send contact controller command"""
    send_message(b"0045;0010;", controller_connection, addr)

def identify_controller(addr=None, controller_connection=None):
    """Send identify controller command"""
    send_message(b"1042;0028;00:06:8E:02:51:3F;", controller_connection, addr)

def controller_information(addr=None, controller_connection=None):
    """Send controller information command"""
    send_message(b"0079;0010;", controller_connection, addr)

def event_message(addr=None, controller_connection=None):
    """Send event message command"""
    send_message(b"1061;0010;", controller_connection, addr)

def card_status(card_id="1334", addr=None, controller_connection=None):
    """Send card status command"""
    send_message(f"0076;0014;{card_id}".encode(), controller_connection, addr)

def card_record(card_id="1234", addr=None, controller_connection=None):
    """Send card record command"""
    send_message(f"0025;0021;{card_id};1;0;0;".encode(), controller_connection, addr)

def get_time_zone(addr=None, controller_connection=None):
    """Send get time zone command"""
    send_message(b"0046;0010;", controller_connection, addr)

def get_card_count(addr=None, controller_connection=None):
    """Send get total cards command"""
    send_message(b"0089;0010;", controller_connection, addr)

def get_time_date(addr=None, controller_connection=None):
    """Send get time date command"""
    send_message(b"0019;0010;", controller_connection, addr)

def get_time_date_alt(addr=None, controller_connection=None):
    """Alternative get time date command"""
    send_message(b"0069;0010;", controller_connection, addr)

def get_all_messages(addr=None, controller_connection=None):
    """Send get/upload all messages command"""
    send_message(b"0063;0010;", controller_connection, addr)


def initialize_connection(addr : str =None, controller_connection=None) -> bool:
    """Initialize connection to the controller"""
    if addr and addr in controller_connection:
        conn = controller_connection[addr]
        if conn:
            try:
                accept_connection(addr, controller_connection)
                controller_information(addr, controller_connection)
                print(f"Initialized connection to {addr}")
                return True
            except Exception as e:
                print(f"Error initializing connection to {addr}: {e}")
    return False

def event_handler(event_data):
    """Handle incoming event data"""
    print(f"Event data: {event_data}")

def user_input():
    while not exit_event.is_set():

        choice = input("Enter choice (1/2/3/q): ")
 
        if   choice  == "0":  send_message(b"0070;0010;")            # accept connection
        elif choice  == "1":  send_message(b"0045;0010;")            # contact controller  
        elif choice  == "00": send_message(b"1042;0028;00:06:8E:02:51:3F;")            # identify Controller
        elif choice  == "2":  send_message(b"0079;0010;")            # controller information
        elif choice  == "3":  send_message(b"1061;0010;")            # Event Message
        elif choice  == "4":  send_message(b"0076;0014;1334")        # card status
        elif choice  == "5":  send_message(b"0025;0021;1234;1;0;0;") # card record
        elif choice  == "6":  send_message(b"0046;0010;")            # Get Time Zone of Controller
        elif choice  == "7":  send_message(b"0089;0010;")            # Get total cards and used cards
        elif choice  == "8":  send_message(b"0019;0010;")            # Get time date
        elif choice  == "9":  send_message(b"0069;0010;")            # Get time date
        elif choice  == "10": send_message(b"0063;0010;")            # Get/upload all msg
        elif choice  == "q":  exit_event.set()
        else: print("Invalid choice, please try again.")

# Main function to start the threads
def event_starter(controller_connection):
    try:
        # Start event server thread
        event_thread = threading.Thread(target=event_server,args=(controller_connection,), daemon=True)
        event_thread.start()

        # Start the user input handling thread
        # input_thread = threading.Thread(target=user_input, daemon=True)
        # input_thread.start()

        # Keep the main thread alive
        # while not exit_event.is_set():
        #     time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nExiting...")
        exit_event.set()

# if __name__ == "__main__":
#     main()


# 1076;0048; 0; 2025/06/24-14:05:46;0;2;0;0;0;1;0;0;