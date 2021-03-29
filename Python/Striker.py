# This function is to be the one that calls all of the other ones in the correct order
import sys

def main(*args):
    # Take in arguments to select what type of graphs to make and tweet
    for arg in args:
        print(arg)

    # Retrieve the data for the desired graph to be made
    print("You have retrieved the data for ...")

    # Create graph from graph library
    print("Generated the graph with the given data")

    # Tweet using the twitter api
    print("Tweeted to your profile")

    # Log when the program was run and if it was successful

if __name__ == "__main__":
    print("So far the arguments I want to be able to take in are as follow:")
    print("--day --week --month --year -d -w -m -y")
    print("And if I think of more I will add them in the future")
    print("You have started the app")
    main(*sys.argv[1:])