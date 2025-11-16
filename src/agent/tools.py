def buildTeamsFeedbackMessage(url: str, group_feedback: str):
    return f"""
    ## 🤖 Scrum Master Feedback & Meeting Takeaways

    Hello Team,

    Thanks for the focused project sync today. I've analyzed the transcript and compiled some key takeaways and constructive feedback, focusing on our Agile practices.

    Here is the Link to the Confluence page :

    {url}

    ### 📝 Group Feedback:

    {group_feedback}

    Best regards,
    Your AI Scrum Master
    """
