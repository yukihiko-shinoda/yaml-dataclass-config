from myproduct import CONFIG


def main() -> None:
    CONFIG.load()
    print(CONFIG.property_a)
    print(CONFIG.property_b)
    if CONFIG.part_config is not None:
        print(CONFIG.part_config.property_c)


if __name__ == '__main__':
    main()
