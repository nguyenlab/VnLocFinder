from qa_model import PersonAnswer, PlaceAnswer, OrganizationAnswer, OrganizationPlaceAnswer, CustomerReview

kb = []

kb.append(PersonAnswer())
kb[-1].name = "Tetsuo Asano"
kb[-1].uri = "http://dbpedia.org/resource/Asano_Tetsuo"
kb[-1].pictureURL = "http://www.jaist.ac.jp/general_info/message/images/president.jpg"

kb.append(PersonAnswer())
kb[-1].name = "Abe Shinzo"
kb[-1].uri = "http://dbpedia.org/resource/Shinz%C5%8D_Abe"


kb.append(PlaceAnswer())
kb[-1].name = "Ishikawa Prefecture"
kb[-1].uri = "http://dbpedia.org/resource/Ishikawa_Prefecture"

# kb.append(OrganizationAnswer())

kb.append(OrganizationPlaceAnswer())
kb[-1].name = "Yawataya Sushi"
kb[-1].telephoneNumber = "+81 761-55-1696"
kb[-1].summary = "Sushi restaurant in a convenient place"
kb[-1].pictureURL = "http://media-cdn.tripadvisor.com/media/photo-s/04/60/cc/ce/five-kinds-of-buri-buri.jpg"
kb[-1].uri = "http://www.tripadvisor.com/Restaurant_Review-g1021241-d7572608-Reviews-Yawataya_Sushi-Nomi_Ishikawa_Prefecture_Chubu.html"
kb[-1].address = "52-17 Mu Ohamamachi, Nomi, Ishikawa Prefecture"
kb[-1].gpsPosition = (36.454994, 136.453720)
cr1 = CustomerReview()
cr1.comments = "Very good place"
cr1.score = 9.0
kb[-1].customerReviews = [cr1]

kb.append(OrganizationPlaceAnswer())
kb[-1].name = "Genshoan"
kb[-1].summary = "Another sushi restaurant"
kb[-1].pictureURL = "http://media-cdn.tripadvisor.com/media/photo-s/04/60/cc/ce/five-kinds-of-buri-buri.jpg"
kb[-1].uri = "http://www.tripadvisor.com/Restaurant_Review-g1021241-d7572645-Reviews-Genshoan-Nomi_Ishikawa_Prefecture_Chubu.html"
kb[-1].address = "1 Shimonogomachi Saru, Nomi, Ishikawa Prefecture"
kb[-1].gpsPosition = (36.439926, 136.452805)
cr1 = CustomerReview()
cr1.comments = "Very good place"
cr1.score = 10.0
cr2 = CustomerReview()
cr2.comments = "Good place"
cr2.score = 7.0
kb[-1].customerReviews = [cr1, cr2]