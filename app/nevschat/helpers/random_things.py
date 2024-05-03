import random
import time

random.seed(time.time())

MIN_AGE = 3
MAX_AGE = 60

FAMILY_NAMES = [
    "三宅",
    "三浦",
    "上村",
    "上田",
    "中島",
    "中川",
    "中村",
    "中沢",
    "中西",
    "中野",
    "丸山",
    "久保",
    "久保田",
    "亀田",
    "五十嵐",
    "井上",
    "井手",
    "今井",
    "伊東",
    "伊藤",
    "佐々木",
    "佐々木",
    "佐久間",
    "佐藤",
    "佐野",
    "児玉",
    "前川",
    "前田",
    "加藤",
    "古屋",
    "古川",
    "古田",
    "古谷",
    "吉川",
    "吉本",
    "吉田",
    "吉野",
    "向井",
    "和田",
    "城戸",
    "堀",
    "堀内",
    "堀口",
    "堀田",
    "夏目",
    "大塚",
    "大島",
    "大森",
    "大西",
    "大野",
    "太田",
    "奥田",
    "宇野",
    "安田",
    "宮崎",
    "宮本",
    "富永",
    "富田",
    "小島",
    "小川",
    "小林",
    "小池",
    "小田",
    "小野寺",
    "山下",
    "山口",
    "山崎",
    "山本",
    "山田",
    "岡崎",
    "岡本",
    "岡田",
    "岡野",
    "岩崎",
    "岩田",
    "川口",
    "川崎",
    "川村",
    "川越",
    "市川",
    "平山",
    "廣田",
    "後藤",
    "戸塚",
    "戸田",
    "手塚",
    "新井",
    "新宿",
    "星野",
    "有馬",
    "服部",
    "望月",
    "朝倉",
    "本多",
    "本田",
    "本間",
    "杉山",
    "杉本",
    "杉浦",
    "村山",
    "松下",
    "松井",
    "松尾",
    "松岡",
    "松崎",
    "松田",
    "柏木",
    "柳",
    "桜井",
    "梶山",
    "森下",
    "森山",
    "森田",
    "榎本",
    "樋口",
    "横山",
    "横田",
    "橋本",
    "水谷",
    "江口",
    "沢田",
    "河野",
    "浅野",
    "浜田",
    "清水",
    "渡辺",
    "滝本",
    "烏山",
    "熊谷",
    "片岡",
    "玉川",
    "田上",
    "田中",
    "田口",
    "田口",
    "田所",
    "田村",
    "田沢",
    "田畑",
    "田辺",
    "畑",
    "白井",
    "白石",
    "相田",
    "石井",
    "石原",
    "石垣",
    "石山",
    "石川",
    "石橋",
    "石田",
    "石黒",
    "福岡",
    "福本",
    "福田",
    "竹下",
    "竹中",
    "竹内",
    "竹田",
    "竹田",
    "細川",
    "若林",
    "菅原",
    "菊池",
    "藤井",
    "藤原",
    "藤田",
    "衣笠",
    "西山",
    "西岡",
    "西川",
    "西川",
    "西村",
    "西田",
    "西野",
    "谷川",
    "辻",
    "野口",
    "野崎",
    "野村",
    "金井",
    "鈴木",
    "鈴木",
    "長尾",
    "長岡",
    "長谷",
    "長谷川",
    "青山",
    "青木",
    "須藤",
    "馬場",
    "高山",
    "高木",
    "高橋",
    "高瀬",
    "高田",
    "高畑",
    "鳥居",
    "黒木",
    "黒田",
]

MALE_NAMES = [
    "修司",
    "健太",
    "優",
    "光",
    "光太",
    "公平",
    "円",
    "剛",
    "功",
    "勇気",
    "勝",
    "勝也",
    "友樹",
    "和樹",
    "哲也",
    "啓太",
    "大樹",
    "大翔",
    "大輝",
    "太一",
    "太郎",
    "太陽",
    "将太",
    "岳",
    "峻太",
    "崇",
    "康太",
    "彰",
    "彰",
    "忍",
    "怜",
    "悠",
    "悠人",
    "悠人",
    "悠太",
    "悠真",
    "慎一",
    "慎二",
    "慎吾",
    "拓也",
    "拓斗",
    "拓海",
    "敏夫",
    "昌宏",
    "明浩",
    "春樹",
    "智也",
    "武",
    "武蔵",
    "泰平",
    "泰輝",
    "浦",
    "浩一",
    "浩司",
    "海",
    "海斗",
    "涼太",
    "渉",
    "潤",
    "琢磨",
    "登",
    "直人",
    "直樹",
    "真",
    "真一",
    "真央",
    "真央",
    "瞬",
    "祐也",
    "祐介",
    "祐佑",
    "祐太",
    "祐樹",
    "穂高",
    "竜太",
    "章",
    "翔",
    "翔太",
    "翔平",
    "翼",
    "聡",
    "聡太",
    "良太",
    "裕之",
    "裕太",
    "裕貴",
    "規",
    "誠",
    "貴",
    "貴之",
    "陸",
    "陽斗",
    "隼人",
    "雄大",
    "雄太",
    "雅人",
    "風馬",
    "颯太",
    "駿",
    "駿太",
]

FEMALE_NAMES = [
    "さつき",
    "はるな",
    "まどか",
    "ゆりか",
    "るみ",
    "レナ",
    "七海",
    "久子",
    "光",
    "光",
    "公子",
    "典子",
    "千佳",
    "千尋",
    "千恵",
    "咲",
    "夏子",
    "夏希",
    "夏美",
    "奈緒",
    "宝",
    "小春",
    "巧美",
    "幸",
    "幸子",
    "幸子",
    "幸恵",
    "弥生",
    "彩香",
    "恵",
    "恵美",
    "愛子",
    "愛莉",
    "愛菜",
    "憂奈",
    "文子",
    "日向",
    "明子",
    "明日香",
    "春",
    "智子",
    "栞",
    "桃子",
    "桜",
    "楓",
    "歩美",
    "沙也香",
    "浩子",
    "涼可",
    "清子",
    "渚",
    "澪",
    "玲",
    "珠希",
    "理香",
    "由布子",
    "由美子",
    "百合",
    "百合子",
    "百合絵",
    "真理",
    "真理子",
    "真紀",
    "真美",
    "瞳",
    "礼子",
    "空",
    "紀子",
    "純子",
    "紗由理",
    "結衣",
    "結香",
    "絵里",
    "絵里菜",
    "綾乃",
    "緑",
    "美和子",
    "美咲",
    "美咲",
    "美奈子",
    "美恵",
    "美春",
    "美羽",
    "美貴",
    "舞",
    "花子",
    "茜",
    "莉子",
    "莉緒",
    "菜々",
    "菫",
    "萌",
    "裕美",
    "貴子",
    "遥",
    "里菜",
    "陽子",
    "陽菜",
    "雪",
    "香菜",
]

CITIES = [
    "東京",
    "横浜",
    "大阪",
    "京都",
    "札幌",
    "神戸",
    "名古屋",
    "広島",
    "福岡",
    "仙台",
    "奈良",
    "金沢",
    "横須賀",
    "岡山",
    "長崎",
    "熊本",
    "青森",
    "静岡",
    "高松",
    "新潟",
]

PROFESSIONS = [
    "ウェイター/ウェイトレス",
    "エンジニア",
    "シェフ",
    "ジャーナリスト",
    "ソーシャルワーカー",
    "ダンサー",
    "ツアーガイド",
    "バリスタ",
    "バーテンダー",
    "パイロット",
    "ファッションデザイナー",
    "プログラマー",
    "メカニック",
    "モデル",
    "会計士",
    "作家",
    "俳優",
    "先生",
    "写真家",
    "刑事",
    "判事",
    "医者",
    "受付係",
    "司書",
    "天文学者",
    "庭師",
    "建築家",
    "建築家",
    "弁護士",
    "心理学者",
    "操縦士",
    "操縦士",
    "政治家",
    "歯医者",
    "消防士",
    "獣医",
    "看護師",
    "科学者",
    "経済学者",
    "翻訳者",
    "芸術家",
    "薬剤師",
    "警察官",
    "農家",
    "造園家",
    "運動選手",
    "配管工",
    "電気技師",
    "音楽家",
    "飛行士",
]

SMALL_CHILDRENS_HOBBIES = [
    "お絵かきシール",
    "かくれんぼ",
    "ぬりえ",
    "ままごと",
    "カラオケ",
    "カルタ",
    "キャッチボール",
    "クッキング",
    "ジグソーパズル",
    "スケッチ",
    "スタンプ集め",
    "ダンス",
    "テント遊び",
    "バルーンアート",
    "ビーズ工作",
    "ブロック遊び",
    "ヘアアクセサリー作り",
    "ペーパークラフト",
    "人形遊び",
    "公園で遊ぶ",
    "列車と遊ぶ",
    "土遊び",
    "寿司作り体験",
    "幼児体操",
    "手品",
    "手遊び歌",
    "折り紙",
    "描画ゲーム",
    "昆虫採集",
    "木登り",
    "歌う",
    "水遊び",
    "玉入れ",
    "石ころ集め",
    "砂遊び",
    "空手体験",
    "粘土遊び",
    "紙飛行機",
    "絵を描く",
    "絵本を読む",
    "羊毛フェルト",
    "自然観察",
    "花を植える",
    "英語の歌",
    "葉っぱ集め",
    "跳び箱",
    "運動会の練習",
    "靴紐結び",
    "音楽会",
    "風船遊び",
]

BIG_CHILDRENS_HOBBIES = [
    "アニメを見る",
    "カラオケ",
    "キャンプ",
    "クイズ",
    "クラフト作り",
    "ゲーム",
    "サイクリング",
    "サッカー",
    "ジグソーパズル",
    "スケート",
    "スケートボード",
    "ダンス",
    "チェス",
    "テニス",
    "ドッジボール",
    "ドローン操作",
    "ハイキング",
    "バイオリンを弾く",
    "バスケットボール",
    "バドミントン",
    "バレエ",
    "ピアノを弾く",
    "フィギュア集め",
    "プログラミング",
    "ヨガ",
    "ロボット製作",
    "写真撮影",
    "切手集め",
    "囲碁",
    "図鑑を見る",
    "園芸",
    "将棋",
    "手品",
    "手芸",
    "折り紙",
    "料理",
    "映画鑑賞",
    "歌うこと",
    "水泳",
    "漫画を読む",
    "科学実験",
    "絵を描く",
    "習字",
    "芸術鑑賞",
    "英会話",
    "読書",
    "野球",
    "釣り",
    "陶芸",
    "馬術",
]

ADOLESCENTS_HOBBIES = [
    "アニメ鑑賞",
    "イラストを描く",
    "カラオケ",
    "ギターを弾く",
    "ゲーム",
    "コスプレ",
    "サッカー",
    "サーフィン",
    "ジョギング",
    "スケートボード",
    "ダンス",
    "ダーツ",
    "チェス",
    "テニス",
    "トランペットを吹く",
    "バイオリンを弾く",
    "バスケットボール",
    "バドミントン",
    "バレーボール",
    "パズルを解く",
    "ピアノを弾く",
    "フィギュアスケート",
    "ベーキング",
    "ボードゲーム",
    "ヨガ",
    "ラグビー",
    "ランニング",
    "写真撮影",
    "囲碁",
    "園芸",
    "将棋",
    "手品",
    "手芸",
    "放送部活動",
    "料理",
    "日記を書く",
    "映画鑑賞",
    "書道",
    "歌を歌う",
    "水泳",
    "漫画を読む",
    "登山",
    "科学実験",
    "絵を描く",
    "習字",
    "自転車に乗る",
    "読書",
    "釣り",
    "陶芸",
    "鳥見",
]

ADULT_HOBBIES = [
    "アイススケート",
    "アイスホッケー",
    "アウトドア",
    "アニメ鑑賞",
    "アメリカンフットボール",
    "アーチェリー",
    "ウィンドサーフィン",
    "ウェイトリフティング",
    "カヌー",
    "カヤッキング",
    "カラオケ",
    "カーリング",
    "クライミング",
    "コスプレ",
    "ゴルフ",
    "サイクリング",
    "サッカー",
    "サバイバルゲーム",
    "サーフィン",
    "サーフィン",
    "ジョギング",
    "スカッシュ",
    "スキー",
    "スキー",
    "スクーター",
    "スケッチ",
    "スケートボーディング",
    "ストリートバスケットボール",
    "スノーボード",
    "スノーボード",
    "ソフトボール",
    "ダンス",
    "テコンドー",
    "テニス",
    "トライアスロン",
    "ハイキング",
    "ハンググライディング",
    "ハンドボール",
    "ハンドボール",
    "バイアスロン",
    "バスケットボール",
    "バドミントン",
    "バレーボール",
    "バードウォッチング",
    "パズル",
    "パラグライディング",
    "ビデオゲーム",
    "ビーエムエックス",
    "フィギュアスケート",
    "フェンシング",
    "ペットの世話",
    "ボウリング",
    "ボクシング",
    "ボルダリング",
    "ボードゲーム",
    "マラソン",
    "マンガ",
    "ヨガ",
    "ヨット",
    "ラグビー",
    "ラジコン",
    "レーシング",
    "ロッククライミング",
    "体操",
    "写真撮影",
    "切手収集",
    "剣道",
    "卓球",
    "合気道",
    "園芸",
    "弓道",
    "手芸",
    "描画",
    "料理",
    "旅行",
    "日本史",
    "星観察",
    "映画鑑賞",
    "書道",
    "柔道",
    "楽器演奏",
    "水泳",
    "登山",
    "相撲",
    "着物着付け",
    "空手",
    "競馬",
    "自動車乗り",
    "自転車競技",
    "花火大会",
    "茶道",
    "読書",
    "野球",
    "野鳥観察",
    "釣り",
    "鉄道模型",
    "陶芸",
    "陸上",
    "陸上競技",
    "音楽鑑賞",
]

FOODS = [
    "うどん",
    "おせち料理",
    "おでん",
    "おにぎり",
    "お好み焼き",
    "お好み焼き",
    "お茶漬け",
    "かき氷",
    "さしみ",
    "ざるそば",
    "しゃぶしゃぶ",
    "しんじょ",
    "すき焼き",
    "そば",
    "そば湯",
    "だんご汁",
    "とんかつ",
    "なめこ汁",
    "ひつまぶし",
    "わらび餅",
    "アイスクリーム",
    "イカ踊り焼き",
    "インスタントラーメン",
    "エビフライ",
    "カステラ",
    "カツサンド",
    "カツサンド",
    "カツ丼",
    "カリフォルニアロール",
    "カレーライス",
    "クッキー",
    "クリームシチュー",
    "クレープ",
    "クレープスズマ",
    "ケーキ",
    "コロッケ",
    "サラダ",
    "サンドイッチ",
    "ショートケーキ",
    "シーフード",
    "シーフードカレー",
    "シーフードパスタ",
    "ジェラート",
    "スイートポテト",
    "ステーキ",
    "タコス",
    "タルト",
    "チュロス",
    "チョコバナナ",
    "チョコフォンデュ",
    "チョコミント",
    "チョコレート",
    "チーズケーキ",
    "ドーナツ",
    "ハンバーガー",
    "ハンバーガーステーキ",
    "バーガー",
    "パイ",
    "パスタ",
    "パフェ",
    "パンケーキ",
    "ビーフシチュー",
    "ピザ",
    "ピザトースト",
    "フライドチキン",
    "フレンチフライ",
    "プリン",
    "プリンアラモード",
    "ホットドッグ",
    "ホットパン",
    "マカロン",
    "マフィン",
    "モンブラン",
    "ラーメン",
    "ラーメン屋のラーメン",
    "ワッフル",
    "串カツ",
    "丼もの",
    "和菓子",
    "大福",
    "天ぷら",
    "寄せ鍋",
    "寿司",
    "寿司巻き",
    "炭火焼き肉",
    "焼き設け",
    "焼き魚",
    "焼き鳥",
    "焼肉",
    "玉子焼き",
    "生姜焼き",
    "田作",
    "白子丼",
    "石焼きビビンバ",
    "蒸し鶏",
    "親子丼",
    "豆腐",
    "豚汁",
    "餃子",
    "鰻丼",
]

DRINKS = [
    "あたたかい水",
    "ほうじ茶ラテ",
    "アサイージュース",
    "アセロラジュース",
    "アップルジュース",
    "イチゴジュース",
    "ウーロン茶",
    "オレンジジュース",
    "カシスオレンジ",
    "カフェラテ",
    "ガムシロップ",
    "キウイジュース",
    "グアバジュース",
    "グレープジュース",
    "ココア",
    "コーヒー",
    "スムージー",
    "ゼロコーラ",
    "ソフトドリンク",
    "ダージリンティー",
    "チャイ",
    "トロピカルジンジャーティー",
    "ハーブティー",
    "パイナップルジュース",
    "パッションフルーツジュース",
    "ペパーミントティー",
    "マンゴージュース",
    "ミルクティー",
    "レモンティー",
    "三重あまおうジュース",
    "京都アイスコーヒー",
    "北海道牛乳",
    "宇治抹茶",
    "岩清水",
    "火入れ蜜柑",
    "炭酸水",
    "烏龍茶",
    "無糖ソーダ",
    "石垣島パインジュース",
    "米麦茶",
    "紅茶",
    "紅茶ラテ",
    "紫イモバブルティー",
    "緑茶",
    "蜜柑ジュース",
    "赤ブドウジュース",
    "野菜ジュース",
    "金時茶",
    "雪見だいふく",
    "霧島炭酸水",
]

MOODS = [
    "がっかりしています。",
    "イライラしています。",
    "ジェラシーを感じています。",
    "リラックスしています。",
    "不安です。",
    "信じています。",
    "冷静です。",
    "刺激されています。",
    "刺激されています。",
    "刺激を求めています。",
    "失望しています。",
    "好奇心が強いです。",
    "孤独を感じています。",
    "希望しています。",
    "平和です。",
    "幸せです。",
    "弱いです。",
    "強いです。",
    "心配しています。",
    "怒っています。",
    "怖がっています。",
    "恐れています。",
    "恥ずかしいです。",
    "悔いています。",
    "悲しいです。",
    "意欲的です。",
    "感動しています。",
    "感謝しています。",
    "慌てています。",
    "憤慨しています。",
    "懐疑的です。",
    "楽しんでいます。",
    "活動的です。",
    "混乱しています。",
    "満足しています。",
    "無精です。",
    "焦っています。",
    "熱狂しています。",
    "甘やかされています。",
    "疑っています。",
    "疲れています。",
    "確信しています。",
    "穏やかです。",
    "緊張しています。",
    "興奮しています。",
    "興奮しています。",
    "落ち込んでいます。",
    "静かです。",
    "騒がしいです。",
    "驚いています。",
]


def get_random_age() -> int:
    return random.randint(MIN_AGE, MAX_AGE)  # nosec


def get_random_name(male: bool) -> str:
    family_name = FAMILY_NAMES[random.randint(0, len(FAMILY_NAMES) - 1)]  # nosec
    if male:
        first_name = MALE_NAMES[random.randint(0, len(MALE_NAMES) - 1)]  # nosec
    else:
        first_name = FEMALE_NAMES[random.randint(0, len(FEMALE_NAMES) - 1)]  # nosec
    return f"{family_name}{first_name}"


def get_random_city() -> str:
    return CITIES[random.randint(0, len(CITIES) - 1)]  # nosec


def get_random_profession(age: int) -> str:
    match age:
        case age if 0 <= age < 3:
            return "ママとずっと一緒にいる赤ちゃん"
        case age if 3 <= age < 6:
            return "幼稚園生"
        case age if 6 <= age < 12:
            return "小学生"
        case age if 12 <= age < 15:
            return "中学生"
        case age if 15 <= age < 18:
            return "高等学生"
        case age if 18 <= age < 21:
            if random.choice([True, False, False]):  # nosec
                return "大学生"
    return PROFESSIONS[random.randint(0, len(PROFESSIONS) - 1)]  # nosec


def get_random_hobbies(age: int) -> str:
    hobbies = random.sample(  # nosec
        (
            SMALL_CHILDRENS_HOBBIES
            if age < 6
            else BIG_CHILDRENS_HOBBIES if age < 13 else ADOLESCENTS_HOBBIES
        ),
        random.randint(2, 4),  # nosec
    )
    return "と".join(hobbies)


def get_random_foods_and_drinks() -> str:
    foods = random.sample(FOODS, random.randint(1, 2))  # nosec
    drinks = random.sample(DRINKS, random.randint(1, 2))  # nosec
    return "と".join(foods + drinks)


def get_random_mood() -> str:
    return MOODS[random.randint(0, len(MOODS) - 1)]  # nosec


def get_random_pitch(age: int) -> float:
    assert MIN_AGE <= age <= MAX_AGE
    match age:
        case age if age < 12:
            return 6
        case age if 12 <= age < 15:
            return 4
        case age if 15 <= age < 18:
            return 2
        case age if 18 <= age < 21:
            return 0
        case age if 21 <= age < 30:
            return -5
        case age if 30 <= age < 40:
            return -10
        case age if 40 <= age < 50:
            return -15
        case _:
            return -20


def get_random_speaking_rate() -> float:
    return random.uniform(0.6, 1.2)  # nosec
