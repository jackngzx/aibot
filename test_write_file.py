from functions.write_file import write_file


def run_all_test_cases():
    result1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    result2 = write_file(
        "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"
    )
    result3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")

    print(result1)
    print(result2)
    print(result3)


run_all_test_cases()

