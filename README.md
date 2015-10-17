# Domain / IP Enumeration

Program to enumerate domain and IP from a list of keywords. This program uses the following information sources:

* Stage 1: Google, Bing 
* Stage 2: Robtex

# Install 

1. Create Environment (optional)

2. Install dependencies:

	pip -r install/requirements.txt

3. Get an API Key for websearch queries

4. Set the API at "BING_API_KEY" in file: config.py

# How to use it ?
 
1. Define a list of keywords to search for at the Stage 1 sites.
 
	Use the file: keywords/websearch_keywords.txt
 
2. Run the program: python enum.py

3. Check results at:
 
	Final Results: results/domains.txt and results/networks.txt
	Stages: results/stage1 and results/stage2
