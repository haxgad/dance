from classifiers import classifier, classifierHarsh
from time import ctime, sleep
from sys import exit
from utils import ResultAccumulator

if __name__ != '__main__':
    print("Run the main module!")
    exit(1)

# Reads the model first and creates a preprocessor.

# Instantiate a result accumulator.

#names of moves
#doublepump, cowboy, crab, chicken, raffles, jamesbond, runningman, hunchback, mermaid, snake, neutral?, final?

accumulator = ResultAccumulator(classes)

# Creates a processor for input data.
#5 sensors - 2 hands, 2 knees, one on back


x_columns = ["mean_leftHandAcclX", "mean_leftHandAcclY", "mean_leftHandAcclZ",
            "mean_rightHandAcclX", "mean_rightHandAcclY", "mean_rightHandAcclZ"
             "mean_leftLegAcclX", "mean_leftLegAcclY", "mean_leftLegAcclZ",
             "mean_rightLegAcclX", "mean_rightLegAcclY", "mean_rightLegAcclZ",
             "mean_BodyX", "mean_BodyY", "mean_BodyZ",
             ]
             
server_ip = #
server_port = #
server_aes_key = #
processor = #

while True: #forever loops, find way to exit programme - neutral move? finishing move?
    # Starts a new iteration with current time printed out.
    print("Enter a new iteration of capturing: ", ctime())

    # Predicts the output according to the input.
    input_data = processor.get_data()
    result = classifier.predict_once(input_data)
    print("The prediction result is", result)

    # Accumulates the result and sees whether it reaches the threshold.
    if accumulator.add(result):
        # Clears the accumulator.
        accumulator.clear_all()

        # Exits from the loop if this is the logout action.
        if result == "logout":
            processor.send_result(result)
            break
        elif result == "stationary":
            print("Detected as stationary state")
        else:
            print("Going to send the result '%s' to remote server." % result)
            processor.send_result(result)

            # Sleeps 1 seconds to give response time for the dancer.
            sleep(1)

    # Sleeps for a certain period to wait for the next iteration to begin.
    sleep(0.2)

print("Thanks for using the DanceDance system!")

exit()
