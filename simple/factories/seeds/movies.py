from simple.factories.movie import MovieFactory
from simple.models.models import MovieCategory


def create_movies():

    action = MovieCategory.objects.get(slug="action")
    adventure = MovieCategory.objects.get(slug="adventure")
    comedy = MovieCategory.objects.get(slug="comedy")
    drama = MovieCategory.objects.get(slug="drama")
    fantasy = MovieCategory.objects.get(slug="fantasy")
    horror = MovieCategory.objects.get(slug="horror")
    mystery = MovieCategory.objects.get(slug="mystery")

    MovieFactory.create(
        title="Inception",
        description=(
            "A thief who steals corporate secrets through the use of dream-sharing "
            "technology is given the inverse task of planting "
            "an idea into the mind of a CEO."
        ),
        release_date="2010-07-16",
        duration_minutes=148,
        rating=8.8,
        director="Christopher Nolan",
        category=action,
        slug="inception",
        is_active=True,
    )

    MovieFactory.create(
        title="Quantum Horizons",
        description=(
            "In a near future where quantum computing has revolutionized society, "
            "a brilliant physicist discovers a way to manipulate time itself, "
            "but faces moral dilemmas when governments seek to "
            "weaponize the technology."
        ),
        release_date="2025-09-15",
        duration_minutes=162,
        rating=None,
        director="Denis Villeneuve",
        category=fantasy,
        slug="quantum-horizons",
        is_active=False,
    )

    MovieFactory.create(
        title="The Matrix",
        description=(
            "A computer hacker learns from mysterious rebels "
            "about the true nature of his reality and his role "
            "in the war against its controllers."
        ),
        release_date="1999-03-31",
        duration_minutes=136,
        rating=8.7,
        director="Lana Wachowski, Lilly Wachowski",
        category=action,
        slug="the-matrix",
        is_active=True,
    )
    MovieFactory.create(
        title="Interstellar",
        description=(
            "A team of explorers travel through a wormhole in "
            "space in an attempt to ensure humanity's survival."
        ),
        release_date="2014-11-07",
        duration_minutes=169,
        rating=8.6,
        director="Christopher Nolan",
        category=adventure,
        slug="interstellar",
        is_active=True,
    )
    MovieFactory.create(
        title="The Dark Knight",
        description=(
            "When the menace known as the Joker emerges from his mysterious past, "
            "he wreaks havoc and chaos on the people of Gotham."
        ),
        release_date="2008-07-18",
        duration_minutes=152,
        rating=9.0,
        director="Christopher Nolan",
        category=action,
        slug="the-dark-knight",
        is_active=True,
    )
    MovieFactory.create(
        title="Pulp Fiction",
        description=(
            "The lives of two mob hitmen, a boxer, a gangster's wife, and a "
            "pair of diner bandits intertwine in four tales of violence and redemption."
        ),
        release_date="1994-10-14",
        duration_minutes=154,
        rating=8.9,
        director="Quentin Tarantino",
        category=comedy,
        slug="pulp-fiction",
        is_active=False,
    )
    MovieFactory.create(
        title="The Shawshank Redemption",
        description=(
            "Two imprisoned isnocents bond over a number of years, finding solace "
            "and eventual redemption through acts of common decency."
        ),
        release_date="1994-09-23",
        duration_minutes=142,
        rating=9.3,
        director="Frank Darabont",
        category=drama,
        slug="the-shawshank-redemption",
        is_active=True,
    )
    MovieFactory.create(
        title="Forrest Gump",
        description=(
            "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate "
            "scandal and other historical events unfold through the perspective of an."
        ),
        release_date="1994-07-06",
        duration_minutes=142,
        rating=8.8,
        director="Robert Zemeckis",
        category=drama,
        slug="forrest-gump",
        is_active=False,
    )
    MovieFactory.create(
        title="The Godfather",
        description=(
            "An organized crime dynasty's aging patriarch transfers control of"
            "his clandestine empire to his reluctant son."
        ),
        release_date="1972-03-24",
        duration_minutes=175,
        rating=9.2,
        director="Francis Ford Coppola",
        category=drama,
        slug="the-godfather",
        is_active=True,
    )
    MovieFactory.create(
        title="Fight Club",
        description=(
            "An insomniac office worker and a devil-may-care soap maker form an "
            "underground fight club that evolves into something much, much more."
        ),
        release_date="1999-10-15",
        duration_minutes=139,
        rating=8.8,
        director="David Fincher",
        category=comedy,
        slug="fight-club",
        is_active=True,
    )
    MovieFactory.create(
        title="The Lord of the Rings: The Return of the King",
        description=(
            "Gandalf and Aragorn lead the World's Free Peoples against Sauron's "
            "army to draw his gaze from Frodo and Sam as they "
            "approach Mount Doom with the One Ring."
        ),
        release_date="2003-12-17",
        duration_minutes=201,
        rating=8.9,
        director="Peter Jackson",
        category=fantasy,
        slug="the-lord-of-the-rings-the-return-of-the-king",
        is_active=False,
    )
    MovieFactory.create(
        title="The Social Network",
        description=(
            "As Harvard students, Eduardo Saverin and Mark Zuckerberg co-found the "
            "social-networking site that would become known as Facebook but the "
            "duo soon find themselves at the center of a whirlwind of fame, "
            "fortune, betrayal, and lawsuits."
        ),
        release_date="2010-10-01",
        duration_minutes=120,
        rating=7.7,
        director="David Fincher",
        category=mystery,
        slug="the-social-network",
        is_active=True,
    )
    MovieFactory.create(
        title="The Silence of the Lambs",
        description=(
            "A young F.B.I. cadet must confide in an incarcerated and manipulative "
            "killer to receive his help on catching another serial killer "
            "who skins his victims."
        ),
        release_date="1991-02-14",
        duration_minutes=118,
        rating=8.6,
        director="Jonathan Demme",
        category=horror,
        slug="the-silence-of-the-lambs",
        is_active=True,
    )
    MovieFactory.create(
        title="Gladiator",
        description=(
            "A former Roman General sets out to exact vengeance against "
            "the corrupt emperor who murdered his family and sent him"
        ),
        release_date="2000-05-05",
        duration_minutes=155,
        rating=8.5,
        director="Ridley Scott",
        category=action,
        slug="gladiator",
        is_active=True,
    )
