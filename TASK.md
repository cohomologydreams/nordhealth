# Nordhealth AI Recruitment Task

## Background

Provet Cloud, our main product, is our SaaS suite of tools required to run veterinary practice.

One of the features (& most common workflows) is consultations. During a scheduled appointment our users can fill in 
patients consultation cards with all details regarding that consultation - this can be the medicine administered, 
treatments performed, observation notes, etc.

After the patient is done with the consultation he usually recieves discharge notes - a set of simple instructions 
summarizing what happened during the consultations and what are the next steps the patient should take.

## Your task

Writing these discharge notes is mundane and takes time. Your task is to automate it.

Write a script that uses a LLM to automatically generate discharge note given the consultation data. Your script should 
accept only one argument: a path to a JSON file containing data from a consultation.

It should output a JSON that contains the key `discharge_note`, for example:

```json
{
  "discharge_note": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ..."
}
```

You have a few examples in the `data/` directory which you can use to test your solution.

Solving this problem should take you no more than 2 hours.

## Requirements

* You can use any LLM provider of your choice
* For each test file in `data/` please include a corresponding output json file in `solution/`.
* Once you're done please create submit your solution to a github/gitlab repository and provide us with the link.
* API tokens to LLM provider should NOT be committed to the repository. 
  Your script should read them from environment variables or a config file.

For all things that you come up with that aren't covered within the requirements above - we trust your judgement to 
make the right decision. The solution is not meant to be perfect, but please try to do your best.

