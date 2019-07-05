from myproduct import CONFIG


def main():
    CONFIG.load()
    print(CONFIG.property_a)
    print(CONFIG.property_b)
    print(CONFIG.part_config.property_c)


if __name__ == '__main__':
    main()
