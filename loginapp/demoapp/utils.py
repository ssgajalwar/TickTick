from slugify import slugify

def unslugify(slug):
    return slugify(slug, separator='_')  # Use the same separator you used in slugify

# Example usage:
original_course_name = unslugify('data-analysis')
print(original_course_name)
# Output: Data Analysis
