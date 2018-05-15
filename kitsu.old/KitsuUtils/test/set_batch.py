lines =[]

if __name__ == "__main__":
    with open("x3650m5-20171027.pasu.bat", "r+") as batch_file:
        for line in batch_file:
            if not "loaddefault" in line:
                lines.append("set {}".format(line.replace('=', ' ')))
            else:
                lines.append(line.replace('=', ' '))

        batch_file.seek(0)
        batch_file.writelines(lines)

