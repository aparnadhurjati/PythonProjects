# import unittest
# from unittest.mock import patch

# # Import your modules here
# from triage.crew import Triage
# from triage.main import run

# class TestBugTriage(unittest.TestCase):

#     def setUp(self):
#         # Example input bug report data
#         self.inputs = {
#             "title": "Submit button missing",
#             "description": "Submit button is not visible on the form.",
#             "steps_to_reproduce": "1. Open form\n2. Check for submit button",
#             "logs": "N/A",
#             "expected_output": "Submit button is visible and clickable",
#             "actual_output": "No submit button displayed"
#         }

#     @patch("crew.crew")  # patch the crew function to mock actual call
#     def test_crew_kickoff_called_with_correct_inputs(self, mock_crew):
#         # Setup mock crew kickoff to return a dummy output
#         mock_crew().kickoff.return_value = {
#             "bug_classification": "UI"
#         }

#         # Call your main function (which should internally call crew.kickoff)
#         run()

#         # Assert kickoff called with correct inputs
#         mock_crew().kickoff.assert_called_once_with(inputs=self.inputs)

#         # Assert the output classification is returned or processed correctly
#         self.assertEqual(result["bug_classification"], "UI")

    

# if __name__ == "__main__":
#     unittest.main()
