
class Examination:
    @staticmethod
    def get_examinations():
        return [
            ("1", "Żyła odpiszczelowa - I st."),
            ("2", "Żyła odpiszczelowa - II st."),
            ("3", "Żyła odpiszczelowa - III st."),
            ("4", "Żyła odpiszczelowa - IV st."),
            ("5", "Żyła odstrzałkowa - I st."),
            ("6", "Żyła odstrzałkowa - II st."),
            ("7", "Żyła odstrzałkowa - III st."),
        ]

    @staticmethod
    def get_examination(value):
        return list(filter(lambda e: e[0] == value, Examination.get_examinations()))[0]
