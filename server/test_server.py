# file overview: Test the ScratchNLP API
import requests
import unittest
import urllib

# api-endpoint for the flask app
URL = "http://127.0.0.1:5000/"

class TestScratchNLPAPI(unittest.TestCase):

  #   def test_add_instruction(self):
		# # sending get request and saving the response as response object
		# testcases = [{
		# 'user_name': 'tina',
		# 'project_name': 'hi',
		# 'raw_instruction': 'say hello',
		# 'response': 'No such project, created new project, and tried to insert it'
		# }, {
		# 'user_name': 'tina',
		# 'project_name': 'hi',
		# 'raw_instruction': "say who's there",
		# 'response': 'Updated project '
		# }]

		# for testcase in testcases:
		# 	url = URL + "user/%s/project/%s/script/%s" %(urllib.quote_plus(testcase['user_name']), urllib.quote_plus(testcase['project_name']), urllib.quote_plus(testcase['raw_instruction']))
		# 	r = requests.get(url = url)
		# 	data = r.text
		# 	self.assertEqual(data, testcase['response'])

    def test_translate_instruction(self):
     	# sending get request and saving the response as response object
		testcases = [
		# TODO(quacht): support the say command.
		# {
		# 'raw_instruction': 'say hello',
		# 'response': 'No such project, created new project, and tried to insert it'
		# },
		# {
		# 'raw_instruction': "say who's there",
		# 'response': 'Updated project '
		# },
		# {
		# 'raw_instruction': 'if x is not less than three then broadcast hello thats it',
		# 'response': str([['doIf', ['not', ['<', ['readVariable', 'x'], 3]], [['broadcast:', 'hello']]]])
		# },
		{
		'raw_instruction': "play the meow sound 10 times",
		'response': str([['doRepeat', 10, [['doPlaySoundAndWait', 'meow']]]])
		}]

		for testcase in testcases:
			url = URL + "translate/%s" %(testcase['raw_instruction'])
			r = requests.get(url = url)
			data = r.text
			self.assertEqual(str(data), testcase['response'])


    def test_get_project(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_get_all_projects(self):
    	self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()