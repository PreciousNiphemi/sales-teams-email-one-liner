import os
import csv
import json
from openai import OpenAI
from outscraper import ApiClient
from dotenv import load_dotenv

load_dotenv(dotenv_path='env/local.env')

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_KEY"),
)
api_client = ApiClient(api_key=os.getenv("OUTSCRAPER_KEY"))

default_beginning_text = "I saw your review from "
default_ending_text = "It seems you guys are really popular in the area with the number of 5 star reviews you have"

# Define your examples here
first_short_example = [
          {
            "customerName": "Pat Rella",
            "customerReview":
              "After discovering a leak around my hot water heater yesterday, a Sunday, I e-mailed and followed up with a call to Woodhaven Plumbing. Keith got back to me very promptly and installed my heater today.\n" +
              "\n" +
              "The old heater was installed by Woodhaven in 2009 and I remember how personable and competent the workers were. I was not disappointed. The owner, Keith arrived as did his son. This establishment is a third generation family business. I recommend them wholeheartedly.",
          },
          {
            "customerName": "Lynn Elfe",
            "customerReview":
              "I needed to have a leaky sink drain repaired and toilet flow regulator replaced. Keith and his partner were very professional, down to earth, up front and honest. They were quick in resolving and completing the repairs. Rates were reasonable as well. I am Very satisfied with their work and would highly recommend to anyone needing a reliable plumber. Thanks!",
          },
          {
            "customerName": "Anita Auricchio",
            "customerReview":
              "My shower pipe broke and needed to be\n" +
              "replaced. This was my first time using there service. They were extremely professional and knowledgeable.\n" +
              "Everything you would require from a plumbing company. As a result I will be using them going forward. Highly recommend.\n" +
              "Anita",
          },
          {
            "customerName": "Amit Patel",
            "customerReview":
              "In Sept 2021, my mother’s basement was flooded with 36 inches of water and NGRID tagged my mother’s water heater and boiler as hazardous and needed to be replaced.  I called approximately 3-4 licensed plumbers and decided on Woodhaven Plumbing.  They were not the most expensive or the cheapest, however, Keith, who is the owner, 4th generation, showed up on time and got back to me with pricing in a timely manner.  Since my mother was out of town, I needed to make sure that there was hot water when she was back.  I communicated that to all and Keith committed and delivered on my priority and started on the boiler and completed that over the next 10 days.  He showed up when he said he would, and did not price gouge.  He was fair and conducted business in a very professional manner.  I highly recommend Woodhaven Plumbing, as they deliver what they promise and are very knowledgeable",
          },
          {
            "customerName": "Nigel Chamblin",
            "customerReview":
              "Keith is a great Master plumber !! He was at my house early, and was personable. He diagnosed the problems with the furnace and was done in an hour. One of the problems was difficult but he was successful. He worked in an efficient manner, as I was right there observing . Keith also cleaned up after himself. The bill was reasaonble for the work performed. I am very pleased with this transaction and will call on him again when needed. I would highly recommend Keith and this company. No BS, no overcharge. I appreciate his professionalism.",
          },
        ];

second_short_example = [
          {
            "customerName": "John Rushton",
            "customerReview":
              "Serve-Well plumbing is reliable, professional, responsive, and fast! Highly recommend this company especially when you’re in a bind and dealing with an emergency.  Thomas S. is my go-to plumber, he is very knowledgeable! I recommend requesting him and his team.  They successfully replaced my water heater when it went, fixed a leak in the shower behind the wall and many other little things. Always on call, always shows ups, and always gets the job done!",
          },
          {
            "customerName": "enza mangano",
            "customerReview":
              "Needed a plumber right away after having a gas leak. I called and they came the very next morning. Once they were done, they explained everything they did. Thank you for a job well done! Thanks Tom and Frederick. Definitely recommend!",
          },
          {
            "customerName": "Samuel Santana",
            "customerReview":
              "Had my boiler replaced in August of this year. They where very professional, clean and friendly. Fred was very nice as well. Thank you all my concerns where addressed. Would definitely recommend there services.",
          },
          {
            "customerName": "A. Rodriguez",
            "customerReview":
              "After my water pipes were banging and rattling, we couldn't figure out the problem! I called Serve-Well and they responded quickly.  I gave a set time and Tommy showed up. Not only did he assess every possibility, but he found the problem and fixed it! He also installed a new digital thermostat (I had an old, broken analog thermostat). I highly recommend Tommy/Serve-Well for your plumbing/heating needs!",
          },
          {
            "customerName": "Thomas McCarthy",
            "customerReview":
              "Great company. They were very responsive. They arrived within 90 minutes of my call. I thought this was fast considering it was not an emergency.\n" +
              "Tom, the service man was courteous, friendly, helpful, and knowledgeable.\n" +
              "I had a clogged drain and it wasn't an easy job but he kept at it until it was flowing clean. This is my new go to plumbing company.",
          },
        ];


third_short_example = [
          {
            "customerName": "Sherana Mohammed",
            "customerReview":
              "My experience with Jerry's plumbing was amazing from start to finish.  Went through alot of different people who wasn't able to fix my boiler issues. Jerry came in and within hours I had another boiler installed.  Him and his crew were very knowledgeable and also cleaned up after which none of the other companies did. Their professionalism was of the charts and I would definitely recommend them to everyone and use them again in the future.",
          },
          {
            "customerName": "Moises Salgado",
            "customerReview": "I had Jerry's Plumbing & HVAC today service my boiler. They sent someone new to heating who just changed the Intermittent Pilot Ignition (it's a $75 part). It was not a heating emergency as its 50 degrees out and its a workday. The service person who was very polite and professional was clearly learning on the job and was calling Jerry - the owner the entire job to be walked through the installation. He was there about 2 hours and charged me $875, which I consider and exorbitant price as clearly the person he sent was training in heating and I should not have been charged for training time. I called Jerry after paying him and let him know that $400 per hour was an exorbitant rate for just changing this 'plug and play' $75 igniter on a new boiler and that per a friend in the HVAC business the whole job including getting the part should have been about an hour including travel time to obtain the part- the total charge should have been around $400. Jerry stood by his billing when I called him and defended his $875 price. I manage several buildings in Queens and will NOT recommend or do business with this business again.",
          },
          {
            "customerName": "Steven Dietz",
            "customerReview":
              "Jerry responded quickly to my late afternoon call and had me send pictures of my water heater with measurements. He was able to come out the next morning and do the work. Only had to suffer less than 24 hours without hot water. Jerry replaced broken water heater with new AO Smith in two hours and everything looks and functions well. I would call Jerry again next time I need a plumber.",
          },
          {
            "customerName": "Frank Mancuso",
            "customerReview":
              "I was very impressed with Jerry's knowledge of the whole gas issue when national grid found a gas leak and he had to replace all the old galvanized piping that I had in this old house. He explained everything step by step, the process of filing the permits with the city and getting approval with the building department. He also had to replace my old boiler system. He installed that in several hours. He was on time and always understood my concern about causing  damage to my house. I highly recommend him and I know I will be using him in the future.",
          },
          {
            "customerName": "Andrew Guida",
            "customerReview":
              "Jerry's installation work is beautiful.  His price was fair and he has a wealth of information that he offers for free.  He is my plumber now, I wouldn't bother calling anyone else.  He even came back a month after installation to help me correct a noisy pipe issue and he did not charge me.  That is above and beyond what most companies would do.",
          },
        ]

fourth_short_example = [
          {
            "customerName": "clara pecoraro",
            "customerReview":
              "Alex and his crew came over and replaced pipes that had been damaged by a service worker. We were so happy to turn our water back on. They were professional and quick and readily came back to insulate the pipes. Great service. I recommend them and will use their services again in the future. Clara in Rosedale",
          },
          {
            "customerName": "Sophia S",
            "customerReview":
              "Alex and his team did an amazing job tuning up my both boilers making sure it’s ready and working as the cold weather approaches. He was very polite and professional. I’m glad I made the right choice trusting Alex and his team.",
          },
          {
            "customerName": "Je'Nyce Bain",
            "customerReview":
              "Alex was efficient and he explained everything as he went along and he was really professional and before he came out he made sure my husband and i weight all our options and when he realized he needed  to come out he keep us updated on his timing and provided amazing service I will use him again with out a doubt. Great work!",
          },
          {
            "customerName": "CAPSULEPILL",
            "customerReview":
              "Alex did a great job, fast reliable and really friendly, would recommend him anytime 👍🏾\n" +
              "\n" +
              "My old water heater pipe rusted and busted, and Alex was able to get it unstuck and install the new one in less then 30 mins",
          },
          {
            "customerName": "Dnesh Ad",
            "customerReview":
              "Super expensive. Find other plumbers. To clean the hot water steam pipe $600. To install new drain pipe of 6 ft. is $2000. NYC should step up and be able to control this unrated prices.",
          },
        ];



def main():
    rows = []
    one_liners = []
    with open('plumbers.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            rows.append(row)

    for i in range(21):
        row = rows[i]
        concatenated_string = f"{row[0]}, {row[7]}, {row[10]}, {row[1]}"
        print("CONCATENATED STRING ", concatenated_string)
        response = api_client.google_maps_reviews([concatenated_string], 5)
        review_data = response[0]['reviews_data']
        review_texts = [{'customerName': review['author_title'], 'customerReview': review['review_text']} for review in review_data]

        print("THE REVIEWS", review_texts)

        business_location = row[10]

        print(" CITY BUSINESS IS LOCATED  --->: ", business_location)

        # Prepare the reviews string
        reviews_string_first = ', '.join([f"reviewer: {review['customerName']}, review: {review['customerReview']}" for review in first_short_example])
        reviews_string_second = ', '.join([f"reviewer: {review['customerName']}, review: {review['customerReview']}" for review in second_short_example])
        reviews_string_third = ', '.join([f"reviewer: {review['customerName']}, review: {review['customerReview']}" for review in third_short_example])
        reviews_string_fourth = ', '.join([f"reviewer: {review['customerName']}, review: {review['customerReview']}" for review in fourth_short_example])


        reviews_string = ', '.join([f"reviewer: {review['customerName']}, review: {review['customerReview']}" for review in review_texts])

        # Call the OpenAI API and generate the one-liner
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful assistant that helps sales team pick the best review from a list of reviews and generate a one-liner starting with 'I' that sounds like something a normal person would say, acknowledging the review, the services offered, and mentioning their location, without using exaggerated compliments?. That ensures the beginning of the one liner starts with {default_beginning_text}, and ends with {default_ending_text} ",
                },
                {
                    "role": "user",
                    "content": f"Here's a list of reviewers and their reviews about a business located at {business_location}: {reviews_string_first}",
                },
                {
                    "role": "assistant",
                    "content": f"{default_beginning_text} Sherana Mohammed. She was really happy with how fast you guys at Jerry's Plumbing fixed her boiler issues in South Richmond Hill. {default_ending_text}",
                },
                 {
                    "role": "user",
                    "content": f"Here's a list of reviewers and their reviews about a business located at {business_location}: {reviews_string_second}",
                },
                {
                    "role": "assistant",
                    "content": f"{default_beginning_text} enza mangano about your company's exceptional service, particularly noting the prompt response and the outstanding work done by your serviceman, Tom. His courteousness, helpfulness, and knowledge truly stood out. {default_ending_text}",
                },
                 {
                    "role": "user",
                    "content": f"Here's a list of reviewers and their reviews about a business located at {business_location}: {reviews_string_third}",
                },
                {
                    "role": "assistant",
                    "content": f"{default_beginning_text} Frank Mancuso's about your plumbing work at South Richmond Hill and he mentioned how you helpd fixed his gas leak and boiler system, and how efficient your service was. {default_ending_text}",
                },
                 {
                    "role": "user",
                    "content": f"Here's a list of reviewers and their reviews about a business located at {business_location}: {reviews_string_fourth}",
                },
                {
                    "role": "assistant",
                    "content": f"{default_beginning_text} Clara in Rosedale who praised how proficiently you and your crew at Alex's Plumbing replaced her damaged pipes in Queens. {default_ending_text}",
                },
                {
                    "role": "user",
                    "content": f"Here's a list of reviewers and their reviews about a business located at {business_location}: {reviews_string}",
                },
                

            ],
        )

        one_liner = completion.choices[0].message.content

        print("THE ON LINER", one_liner)

        # Add one-liner to array
        one_liners.append(one_liner)

    # Create JSON object with all one-liners
    one_liners_json = json.dumps({'one_liners': one_liners})

    # Write JSON to file
    with open('one_liners.json', 'w') as file:
        file.write(one_liners_json)

    print("One-liners saved to one_liners.json")

main()