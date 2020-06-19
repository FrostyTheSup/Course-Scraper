import urllib
import urllib.request
from bs4 import BeautifulSoup
import pprint


def main():
    urls = []
    courses = input("Please enter each course code separated by a space: ").upper().split()
    for course in courses:
        if not validate_code(course):
            print("Please check course codes and try again")
        else:
            urls.extend([course, find_course_info(create_url(course))])
    pprint.pprint(urls)


def create_url(course_code):
    return "http://my.uq.edu.au/programs-courses/course.html?course_code=" + course_code


def validate_code(course_code):
    if len(course_code) == 8 and course_code[:4].isalpha() \
            and course_code[4:].isdigit():
        return True
    else:
        return False


def find_course_info(url):
    info = []
    desired_attributes = ["course-units", "course-contact", "course-incompatible",
                          "course-prerequisite", "course-recommended-prerequisite", "course-summary"]
    attribute_description = ["Units", "Contact Hours", "Incompatable Courses", "Courses Prerequisites",
                             "Recommended Prerequisites", "Summary"]
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    for attr in desired_attributes:
        info.append(sanitise_html(str(soup.find('p', id=attr))))
    course_offerings = []
    course_offerings.extend(
        str(soup.find_all('a', class_="course-offering-year")).replace('\t', '').replace('\n', '').split('>'))
    info = [a + " = " + b for a, b in zip(attribute_description, info)]
    for line in course_offerings:
        if line.startswith("Semester"):
            info.append(line[:-3])
    return info


def sanitise_html(html):
    return html[html.find(">") + 1:html.find("</")]


if __name__ == '__main__':
    main()
