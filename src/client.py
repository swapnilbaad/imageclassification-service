import argparse
import csv
import zmq
import sys

def parse_csv(file_path):
    """
    Parses the CSV file and returns a list of URLs.
    Assumes each row has one URL (in the first column).
    """
    urls = []
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # Skip empty rows
                    urls.append(row[0])
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)
    return urls

def main():
    parser = argparse.ArgumentParser(description='Client for toy-service that sends image URLs and prints classification results.')
    parser.add_argument('csv_file', help='Path to the CSV file containing image URLs')
    args = parser.parse_args()

    # Parse URLs from CSV file
    urls = parse_csv(args.csv_file)
    num_urls = len(urls)
    if num_urls == 0:
        print("No URLs found in the CSV file.")
        sys.exit(1)

    # Create ZeroMQ context
    context = zmq.Context()

    # Set up the REQ socket for sending URLs to the server
    req_socket = context.socket(zmq.REQ)
    req_socket.connect("tcp://localhost:5555")

    # Set up the SUB socket for receiving published results
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect("tcp://localhost:5556")
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages

    # Send the list of URLs as a REQuest
    req_socket.send_json({"urls": urls})
    ack = req_socket.recv_json()
    print("Server Acknowledged:", ack)
    expected_results = ack.get("num_urls", num_urls)

    # Listen for published messages until all results are received
    received = 0
    print("Waiting for classification results...\n")
    while received < expected_results:
        result = sub_socket.recv_json()
        print("Received:", result)
        received += 1

    print("\nAll inferences received.")

    # Clean up
    req_socket.close()
    sub_socket.close()
    context.term()

if __name__ == '__main__':
    main()
