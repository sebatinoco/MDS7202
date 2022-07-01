def praw_reddit(nombre_subreddit="chile", n_hot=1000):
    reddit = praw.Reddit(
        client_id="-w2hyFINxZ8T3g",
        client_secret="zGPCI4s3g6Ic6AsRi7vIpP0NoxbFdw",
        password="ClasesMDS7202",
        user_agent="Clases",
        username="DocenciaDataScience",
        check_for_async=False,
    )
    subreddit = reddit.subreddit(nombre_subreddit)

    votes, post, url = {}, {}, {}
    top_submissions = list(subreddit.hot(limit=n_hot)) # obtenemos el top n de posts del foro
    for it, top_n in enumerate(range(50, len(top_submissions), 50)):
        top_n_submissions = top_submissions[:top_n] # obtiene los primeros 50 posts
        upvotes, downvotes, url[it], post[it] = [], [], [], []

        for submission in top_n_submissions: # para cada uno de los posts
            try:
                ratio = submission.upvote_ratio # obtenemos el ratio de upvote
                ups = int( # calculamos upvotes
                    round((ratio * submission.score) / (2 * ratio - 1))
                    if ratio != 0.5
                    else round(submission.score / 2)
                )
                upvotes.append(ups) # guardamos upvotes
                downvotes.append(ups - submission.score) # guardamos downvotes
                post[it].append(submission.title) # guardamos titulo del post
                url[it].append(submission.url) # guardamos url
            except Exception as e: # en caso de error, sigue 
                continue
        votes[it] = np.array([upvotes, downvotes]).T
    return votes, post, url # retorna votos, post y url

from praw_module import praw_reddit

%mprun -f praw_reddit praw_reddit()
