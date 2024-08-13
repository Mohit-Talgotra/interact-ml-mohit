import json
import logging
import random
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
import uuid

# Assuming connection to PostgreSQL is already established
# Replace these values with your actual database configuration
conn = psycopg2.connect(
    dbname='your_db',
    user='your_user',
    password='your_password',
    host='your_host'
)

def to_lowercase_array(arr):
    return [str.lower() for str in arr]

def random_links():
    links = [
        "https://www.google.com",
        "https://www.youtube.com",
        "https://www.facebook.com",
        "https://www.gmail.com",
        "https://www.github.com"
    ]
    count = random.randint(0, 5)
    random.shuffle(links)
    return links[:count]

def get_random_user(users):
    return random.choice(users)

def get_random_project_id(project_ids):
    return random.choice(project_ids)

def soft_slugify(text):
    return text.lower().replace(" ", "-").replace("/", "-")

def populate_projects():
    logging.info("----------------Populating Projects----------------")
    with open('populate/projects.json', 'r') as file:
        projects = json.load(file)

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()

        if not users:
            return

        cover_pics = [
            "default_1.jpg", "default_2.jpg", "default_3.jpg",
            "default_4.jpg", "default_5.jpg", "default_6.jpg",
            "default_7.jpg", "default_8.jpg", "default_9.jpg"
        ]

        for project in projects:
            user = get_random_user(users)
            project['user_id'] = user[0]
            project['slug'] = soft_slugify(project['title'])
            project['tags'] = to_lowercase_array(project['tags'])
            project['links'] = random_links()

            # Randomly select a cover picture
            project['cover_pic'] = random.choice(cover_pics)
            project['blur_hash'] = 'no-hash'

            columns = project.keys()
            values = [project[column] for column in columns]
            insert_statement = 'INSERT INTO projects (%s) VALUES %s' % (
                ', '.join(columns), tuple(values))
            try:
                cur.execute(insert_statement)
                conn.commit()
                logging.info("Added Project: %s", project['title'])
            except Exception as e:
                logging.error("Failed to insert project: %s", e)
                conn.rollback()

def populate_posts():
    logging.info("----------------Populating Posts----------------")
    with open('populate/posts.json', 'r') as file:
        posts = json.load(file)

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()

        if not users:
            return

        for post in posts:
            post['user_id'] = get_random_user(users)[0]
            columns = post.keys()
            values = [post[column] for column in columns]
            insert_statement = 'INSERT INTO posts (%s) VALUES %s' % (
                ', '.join(columns), tuple(values))
            try:
                cur.execute(insert_statement)
                conn.commit()
            except Exception as e:
                logging.error("Failed to insert post: %s", e)
                conn.rollback()

def populate_openings():
    logging.info("----------------Populating Openings----------------")
    with open('populate/openings.json', 'r') as file:
        openings = json.load(file)

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM projects")
        projects = cur.fetchall()

        if not projects:
            return

        project_ids = [project[0] for project in projects]

        for opening in openings:
            project_id = get_random_project_id(project_ids)
            opening['project_id'] = project_id
            cur.execute("SELECT * FROM projects WHERE id = %s", (project_id,))
            project = cur.fetchone()
            opening['user_id'] = project[1]

            columns = opening.keys()
            values = [opening[column] for column in columns]
            insert_statement = 'INSERT INTO openings (%s) VALUES %s' % (
                ', '.join(columns), tuple(values))
            try:
                cur.execute(insert_statement)
                conn.commit()
                logging.info("Added Opening: %s, in Project %s", opening['title'], project['title'])
            except Exception as e:
                logging.error("Failed to insert opening: %s", e)
                conn.rollback()

def populate_users_and_orgs():
    logging.info("----------------Populating Organisations----------------")
    with open('populate/users.json', 'r') as file:
        users = json.load(file)

    with conn.cursor() as cur:
        for user in users:
            logging.info("Creating User - %s", user['name'])

            new_user = {
                'name': user['name'],
                'email': user['email'],
                'password': user['password'],
                'username': user['username'],
                'tagline': user['tagline'],
                'password_changed_at': datetime.now(),
                'organization_status': user['isOrganization'],
                'tags': user['tags'],
                'links': user['links'],
                'verified': True,
                'onboarding_completed': True,
            }

            columns = new_user.keys()
            values = [new_user[column] for column in columns]
            insert_statement = 'INSERT INTO users (%s) VALUES %s' % (
                ', '.join(columns), tuple(values))
            try:
                cur.execute(insert_statement)
                conn.commit()
            except Exception as e:
                logging.error("Error while creating Org User: %s", e)
                conn.rollback()
                continue

            if new_user['organization_status']:
                logging.info("Creating Org - %s", user['name'])
                organization = {
                    'user_id': new_user['id'],
                    'organization_title': new_user['name'],
                    'created_at': datetime.now(),
                }
                columns = organization.keys()
                values = [organization[column] for column in columns]
                insert_statement = 'INSERT INTO organizations (%s) VALUES %s' % (
                    ', '.join(columns), tuple(values))
                try:
                    cur.execute(insert_statement)
                    conn.commit()
                except Exception as e:
                    logging.error("Error while creating Org: %s", e)
                    conn.rollback()

            logging.info("Creating Profile - %s", user['name'])

            new_profile = {
                'user_id': new_user['id'],
            }
            columns = new_profile.keys()
            values = [new_profile[column] for column in columns]
            insert_statement = 'INSERT INTO profiles (%s) VALUES %s' % (
                ', '.join(columns), tuple(values))
            try:
                cur.execute(insert_statement)
                conn.commit()
            except Exception as e:
                logging.error("Error while creating Profile: %s", e)
                conn.rollback()

            logging.info("Successfully created User - %s", new_user['name'])

def populate_comments():
    logging.info("----------------Populating Comments----------------")
    with open('populate/comments.json', 'r') as file:
        comments = json.load(file)

    with conn.cursor() as cur:
        for comment in comments:
            columns = comment.keys()
            values = [comment[column] for column in columns]
            insert_statement = 'INSERT INTO comments (%s) VALUES %s' % (
                ', '.join(columns), tuple(values))
            try:
                cur.execute(insert_statement)
                conn.commit()
            except Exception as e:
                logging.error("Failed to insert comment: %s", e)
                conn.rollback()

def populate_applications():
    logging.info("----------------Populating Applications----------------")
    with open('populate/applications.json', 'r') as file:
        applications = json.load(file)

    with conn.cursor() as cur:
        for application in applications:
            columns = application.keys()
            values = [application[column] for column in columns]
            insert_statement = 'INSERT INTO applications (%s) VALUES %s' % (
                ', '.join(columns), tuple(values))
            try:
                cur.execute(insert_statement)
                conn.commit()
            except Exception as e:
                logging.error("Failed to insert application: %s", e)
                conn.rollback()

def fill_dummies():
    populate_projects()
    populate_posts()
    populate_openings()
    generate_dummies()

def generate_dummies():
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM users")
        user_ids = cur.fetchall()

        cur.execute("SELECT id FROM posts")
        post_ids = cur.fetchall()

        cur.execute("SELECT id FROM projects")
        project_ids = cur.fetchall()

        cur.execute("SELECT id FROM openings")
        opening_ids = cur.fetchall()

        cur.execute("SELECT id FROM events")
        event_ids = cur.fetchall()

        cur.execute("SELECT id FROM comments")
        comment_ids = cur.fetchall()

    generate_likes(50, user_ids, post_ids, project_ids, event_ids, comment_ids)
    generate_reports(15, user_ids, post_ids, project_ids, event_ids, opening_ids)
    generate_project_memberships(25, user_ids, project_ids)

    generate_bookmarks("post", 20, user_ids, post_ids, project_ids, opening_ids, event_ids)
    generate_bookmarks("project", 20, user_ids, post_ids, project_ids, opening_ids, event_ids)
    generate_bookmarks("opening", 20, user_ids, post_ids, project_ids, opening_ids, event_ids)
    generate_bookmarks("event", 20, user_ids, post_ids, project_ids, opening_ids, event_ids)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname="your_database",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )

# Generate Likes
def generate_likes(n, user_ids, post_ids, project_ids, event_ids, comment_ids):
    conn = get_db_connection()
    cur = conn.cursor()

    likes = []
    for _ in range(n):
        user_id = random.choice(user_ids)

        post_id = project_id = event_id = comment_id = None
        choice = random.randint(0, 3)
        if choice == 0:
            post_id = random.choice(post_ids)
        elif choice == 1:
            project_id = random.choice(project_ids)
        elif choice == 2:
            event_id = random.choice(event_ids)
        elif choice == 3:
            comment_id = random.choice(comment_ids)

        like = (str(uuid.uuid4()), user_id, post_id, project_id, event_id, comment_id)
        likes.append(like)

    query = """
    INSERT INTO likes (id, user_id, post_id, project_id, event_id, comment_id)
    VALUES %s
    """
    try:
        execute_values(cur, query, likes)
        conn.commit()
        logging.info(f"Generated {n} likes.")
    except Exception as e:
        logging.error("Error while creating likes.", e)
    finally:
        cur.close()
        conn.close()

# Generate Bookmarks
def generate_bookmarks(bookmark_type, n, user_ids, post_ids, project_ids, opening_ids, event_ids):
    conn = get_db_connection()
    cur = conn.cursor()

    for i in range(n):
        user_id = random.choice(user_ids)
        title = f"Bookmark {i}"
        bookmark_id = str(uuid.uuid4())

        if bookmark_type == "post":
            query = """
            INSERT INTO post_bookmarks (id, user_id, title) VALUES (%s, %s, %s)
            """
            cur.execute(query, (bookmark_id, user_id, title))

            items = [
                (bookmark_id, random.choice(post_ids))
                for _ in range(10)
            ]
            query = """
            INSERT INTO post_bookmark_items (post_bookmark_id, post_id)
            VALUES %s
            """
            execute_values(cur, query, items)

        elif bookmark_type == "project":
            query = """
            INSERT INTO project_bookmarks (id, user_id, title) VALUES (%s, %s, %s)
            """
            cur.execute(query, (bookmark_id, user_id, title))

            items = [
                (bookmark_id, random.choice(project_ids))
                for _ in range(10)
            ]
            query = """
            INSERT INTO project_bookmark_items (project_bookmark_id, project_id)
            VALUES %s
            """
            execute_values(cur, query, items)

        elif bookmark_type == "opening":
            query = """
            INSERT INTO opening_bookmarks (id, user_id, title) VALUES (%s, %s, %s)
            """
            cur.execute(query, (bookmark_id, user_id, title))

            items = [
                (bookmark_id, random.choice(opening_ids))
                for _ in range(10)
            ]
            query = """
            INSERT INTO opening_bookmark_items (opening_bookmark_id, opening_id)
            VALUES %s
            """
            execute_values(cur, query, items)

        elif bookmark_type == "event":
            query = """
            INSERT INTO event_bookmarks (id, user_id, title) VALUES (%s, %s, %s)
            """
            cur.execute(query, (bookmark_id, user_id, title))

            items = [
                (bookmark_id, random.choice(event_ids))
                for _ in range(10)
            ]
            query = """
            INSERT INTO event_bookmark_items (event_bookmark_id, event_id)
            VALUES %s
            """
            execute_values(cur, query, items)

        else:
            logging.error("Invalid bookmark type:", bookmark_type)

    conn.commit()
    logging.info(f"Generated {n} bookmarks.")
    cur.close()
    conn.close()

# Generate Reports
def generate_reports(n, user_ids, post_ids, project_ids, event_ids, opening_ids):
    conn = get_db_connection()
    cur = conn.cursor()

    reports = []
    for _ in range(n):
        reporter_id = random.choice(user_ids)
        report_type = random.randint(0, 8)

        post_id = project_id = event_id = user_id = opening_id = None
        choice = random.randint(0, 4)
        if choice == 0:
            post_id = random.choice(post_ids)
        elif choice == 1:
            project_id = random.choice(project_ids)
        elif choice == 2:
            event_id = random.choice(event_ids)
        elif choice == 3:
            user_id = random.choice(user_ids)
        elif choice == 4:
            opening_id = random.choice(opening_ids)

        report = (str(uuid.uuid4()), report_type, reporter_id, user_id, post_id, project_id, event_id, opening_id)
        reports.append(report)

    query = """
    INSERT INTO reports (id, report_type, reporter_id, user_id, post_id, project_id, event_id, opening_id)
    VALUES %s
    """
    try:
        execute_values(cur, query, reports)
        conn.commit()
        logging.info(f"Generated {n} reports.")
    except Exception as e:
        logging.error("Error while creating reports.", e)
    finally:
        cur.close()
        conn.close()

# Generate Project Memberships
def generate_project_memberships(n, user_ids, project_ids):
    conn = get_db_connection()
    cur = conn.cursor()

    roles = ["ProjectMember", "ProjectEditor", "ProjectManager"]
    titles = [
        "Lead Developer",
        "Project Coordinator",
        "Team Lead",
        "Senior Developer",
        "Junior Developer",
        "Project Analyst",
        "Product Manager",
        "Technical Lead",
        "Project Supervisor",
        "Quality Assurance",
    ]

    memberships = []
    for _ in range(n):
        user_id = random.choice(user_ids)
        project_id = random.choice(project_ids)
        role = random.choice(roles)
        title = random.choice(titles)

        membership = (str(uuid.uuid4()), project_id, user_id, role, title)
        memberships.append(membership)

    query = """
    INSERT INTO memberships (id, project_id, user_id, role, title)
    VALUES %s
    """
    try:
        execute_values(cur, query, memberships)
        conn.commit()
        logging.info(f"Generated {n} memberships.")
    except Exception as e:
        logging.error("Error while creating memberships.", e)
    finally:
        cur.close()
        conn.close()
