import random
import time

random.seed(time.time())

MIN_AGE = 3
MAX_AGE = 60
MALE_PITCH_CHANGE_SEMITONES = 12
FEMALE_PITCH_CHANGE_SEMITONES = 6

FAMILY_NAMES = [
    '三宅',
    '三浦',
    '上村',
    '上田',
    '中島',
    '中川',
    '中村',
    '中沢',
    '中西',
    '中野',
    '丸山',
    '久保',
    '久保田',
    '亀田',
    '五十嵐',
    '井上',
    '井手',
    '今井',
    '伊東',
    '伊藤',
    '佐々木',
    '佐々木',
    '佐久間',
    '佐藤',
    '佐野',
    '児玉',
    '前川',
    '前田',
    '加藤',
    '古屋',
    '古川',
    '古田',
    '古谷',
    '吉川',
    '吉本',
    '吉田',
    '吉野',
    '向井',
    '和田',
    '城戸',
    '堀',
    '堀内',
    '堀口',
    '堀田',
    '夏目',
    '大塚',
    '大島',
    '大森',
    '大西',
    '大野',
    '太田',
    '奥田',
    '宇野',
    '安田',
    '宮崎',
    '宮本',
    '富永',
    '富田',
    '小島',
    '小川',
    '小林',
    '小池',
    '小田',
    '小野寺',
    '山下',
    '山口',
    '山崎',
    '山本',
    '山田',
    '岡崎',
    '岡本',
    '岡田',
    '岡野',
    '岩崎',
    '岩田',
    '川口',
    '川崎',
    '川村',
    '川越',
    '市川',
    '平山',
    '廣田',
    '後藤',
    '戸塚',
    '戸田',
    '手塚',
    '新井',
    '新宿',
    '星野',
    '有馬',
    '服部',
    '望月',
    '朝倉',
    '本多',
    '本田',
    '本間',
    '杉山',
    '杉本',
    '杉浦',
    '村山',
    '松下',
    '松井',
    '松尾',
    '松岡',
    '松崎',
    '松田',
    '柏木',
    '柳',
    '桜井',
    '梶山',
    '森下',
    '森山',
    '森田',
    '榎本',
    '樋口',
    '横山',
    '横田',
    '橋本',
    '水谷',
    '江口',
    '沢田',
    '河野',
    '浅野',
    '浜田',
    '清水',
    '渡辺',
    '滝本',
    '烏山',
    '熊谷',
    '片岡',
    '玉川',
    '田上',
    '田中',
    '田口',
    '田口',
    '田所',
    '田村',
    '田沢',
    '田畑',
    '田辺',
    '畑',
    '白井',
    '白石',
    '相田',
    '石井',
    '石原',
    '石垣',
    '石山',
    '石川',
    '石橋',
    '石田',
    '石黒',
    '福岡',
    '福本',
    '福田',
    '竹下',
    '竹中',
    '竹内',
    '竹田',
    '竹田',
    '細川',
    '若林',
    '菅原',
    '菊池',
    '藤井',
    '藤原',
    '藤田',
    '衣笠',
    '西山',
    '西岡',
    '西川',
    '西川',
    '西村',
    '西田',
    '西野',
    '谷川',
    '辻',
    '野口',
    '野崎',
    '野村',
    '金井',
    '鈴木',
    '鈴木',
    '長尾',
    '長岡',
    '長谷',
    '長谷川',
    '青山',
    '青木',
    '須藤',
    '馬場',
    '高山',
    '高木',
    '高橋',
    '高瀬',
    '高田',
    '高畑',
    '鳥居',
    '黒木',
    '黒田',
]

MALE_NAMES = [
    '修司',
    '健太',
    '優',
    '光',
    '光太',
    '公平',
    '円',
    '剛',
    '功',
    '勇気',
    '勝',
    '勝也',
    '友樹',
    '和樹',
    '哲也',
    '啓太',
    '大樹',
    '大翔',
    '大輝',
    '太一',
    '太郎',
    '太陽',
    '将太',
    '岳',
    '峻太',
    '崇',
    '康太',
    '彰',
    '彰',
    '忍',
    '怜',
    '悠',
    '悠人',
    '悠人',
    '悠太',
    '悠真',
    '慎一',
    '慎二',
    '慎吾',
    '拓也',
    '拓斗',
    '拓海',
    '敏夫',
    '昌宏',
    '明浩',
    '春樹',
    '智也',
    '武',
    '武蔵',
    '泰平',
    '泰輝',
    '浦',
    '浩一',
    '浩司',
    '海',
    '海斗',
    '涼太',
    '渉',
    '潤',
    '琢磨',
    '登',
    '直人',
    '直樹',
    '真',
    '真一',
    '真央',
    '真央',
    '瞬',
    '祐也',
    '祐介',
    '祐佑',
    '祐太',
    '祐樹',
    '穂高',
    '竜太',
    '章',
    '翔',
    '翔太',
    '翔平',
    '翼',
    '聡',
    '聡太',
    '良太',
    '裕之',
    '裕太',
    '裕貴',
    '規',
    '誠',
    '貴',
    '貴之',
    '陸',
    '陽斗',
    '隼人',
    '雄大',
    '雄太',
    '雅人',
    '風馬',
    '颯太',
    '駿',
    '駿太',
]

FEMALE_NAMES = [
    'さつき',
    'はるな',
    'まどか',
    'ゆりか',
    'るみ',
    'レナ',
    '七海',
    '久子',
    '光',
    '光',
    '公子',
    '典子',
    '千佳',
    '千尋',
    '千恵',
    '咲',
    '夏子',
    '夏希',
    '夏美',
    '奈緒',
    '宝',
    '小春',
    '巧美',
    '幸',
    '幸子',
    '幸子',
    '幸恵',
    '弥生',
    '彩香',
    '恵',
    '恵美',
    '愛子',
    '愛莉',
    '愛菜',
    '憂奈',
    '文子',
    '日向',
    '明子',
    '明日香',
    '春',
    '智子',
    '栞',
    '桃子',
    '桜',
    '楓',
    '歩美',
    '沙也香',
    '浩子',
    '涼可',
    '清子',
    '渚',
    '澪',
    '玲',
    '珠希',
    '理香',
    '由布子',
    '由美子',
    '百合',
    '百合子',
    '百合絵',
    '真理',
    '真理子',
    '真紀',
    '真美',
    '瞳',
    '礼子',
    '空',
    '紀子',
    '純子',
    '紗由理',
    '結衣',
    '結香',
    '絵里',
    '絵里菜',
    '綾乃',
    '緑',
    '美和子',
    '美咲',
    '美咲',
    '美奈子',
    '美恵',
    '美春',
    '美羽',
    '美貴',
    '舞',
    '花子',
    '茜',
    '莉子',
    '莉緒',
    '菜々',
    '菫',
    '萌',
    '裕美',
    '貴子',
    '遥',
    '里菜',
    '陽子',
    '陽菜',
    '雪',
    '香菜',
]

CITIES = [
    '東京',
    '横浜',
    '大阪',
    '京都',
    '札幌',
    '神戸',
    '名古屋',
    '広島',
    '福岡',
    '仙台',
    '奈良',
    '金沢',
    '横須賀',
    '岡山',
    '長崎',
    '熊本',
    '青森',
    '静岡',
    '高松',
    '新潟',
]

PROFESSIONS = [
    'ウェイター/ウェイトレス',
    'エンジニア',
    'シェフ',
    'ジャーナリスト',
    'ソーシャルワーカー',
    'ダンサー',
    'ツアーガイド',
    'バリスタ',
    'バーテンダー',
    'パイロット',
    'ファッションデザイナー',
    'プログラマー',
    'メカニック',
    'モデル',
    '会計士',
    '作家',
    '俳優',
    '先生',
    '写真家',
    '刑事',
    '判事',
    '医者',
    '受付係',
    '司書',
    '天文学者',
    '庭師',
    '建築家',
    '建築家',
    '弁護士',
    '心理学者',
    '操縦士',
    '操縦士',
    '政治家',
    '歯医者',
    '消防士',
    '獣医',
    '看護師',
    '科学者',
    '経済学者',
    '翻訳者',
    '芸術家',
    '薬剤師',
    '警察官',
    '農家',
    '造園家',
    '運動選手',
    '配管工',
    '電気技師',
    '音楽家',
    '飛行士',
]

SMALL_CHILDRENS_HOBBIES = [
    'お絵かきシール',
    'かくれんぼ',
    'ぬりえ',
    'ままごと',
    'カラオケ',
    'カルタ',
    'キャッチボール',
    'クッキング',
    'ジグソーパズル',
    'スケッチ',
    'スタンプ集め',
    'ダンス',
    'テント遊び',
    'バルーンアート',
    'ビーズ工作',
    'ブロック遊び',
    'ヘアアクセサリー作り',
    'ペーパークラフト',
    '人形遊び',
    '公園で遊ぶ',
    '列車と遊ぶ',
    '土遊び',
    '寿司作り体験',
    '幼児体操',
    '手品',
    '手遊び歌',
    '折り紙',
    '描画ゲーム',
    '昆虫採集',
    '木登り',
    '歌う',
    '水遊び',
    '玉入れ',
    '石ころ集め',
    '砂遊び',
    '空手体験',
    '粘土遊び',
    '紙飛行機',
    '絵を描く',
    '絵本を読む',
    '羊毛フェルト',
    '自然観察',
    '花を植える',
    '英語の歌',
    '葉っぱ集め',
    '跳び箱',
    '運動会の練習',
    '靴紐結び',
    '音楽会',
    '風船遊び',
]

BIG_CHILDRENS_HOBBIES = [
    'アニメを見る',
    'カラオケ',
    'キャンプ',
    'クイズ',
    'クラフト作り',
    'ゲーム',
    'サイクリング',
    'サッカー',
    'ジグソーパズル',
    'スケート',
    'スケートボード',
    'ダンス',
    'チェス',
    'テニス',
    'ドッジボール',
    'ドローン操作',
    'ハイキング',
    'バイオリンを弾く',
    'バスケットボール',
    'バドミントン',
    'バレエ',
    'ピアノを弾く',
    'フィギュア集め',
    'プログラミング',
    'ヨガ',
    'ロボット製作',
    '写真撮影',
    '切手集め',
    '囲碁',
    '図鑑を見る',
    '園芸',
    '将棋',
    '手品',
    '手芸',
    '折り紙',
    '料理',
    '映画鑑賞',
    '歌うこと',
    '水泳',
    '漫画を読む',
    '科学実験',
    '絵を描く',
    '習字',
    '芸術鑑賞',
    '英会話',
    '読書',
    '野球',
    '釣り',
    '陶芸',
    '馬術',
]

ADOLESCENTS_HOBBIES = [
    'アニメ鑑賞',
    'イラストを描く',
    'カラオケ',
    'ギターを弾く',
    'ゲーム',
    'コスプレ',
    'サッカー',
    'サーフィン',
    'ジョギング',
    'スケートボード',
    'ダンス',
    'ダーツ',
    'チェス',
    'テニス',
    'トランペットを吹く',
    'バイオリンを弾く',
    'バスケットボール',
    'バドミントン',
    'バレーボール',
    'パズルを解く',
    'ピアノを弾く',
    'フィギュアスケート',
    'ベーキング',
    'ボードゲーム',
    'ヨガ',
    'ラグビー',
    'ランニング',
    '写真撮影',
    '囲碁',
    '園芸',
    '将棋',
    '手品',
    '手芸',
    '放送部活動',
    '料理',
    '日記を書く',
    '映画鑑賞',
    '書道',
    '歌を歌う',
    '水泳',
    '漫画を読む',
    '登山',
    '科学実験',
    '絵を描く',
    '習字',
    '自転車に乗る',
    '読書',
    '釣り',
    '陶芸',
    '鳥見',
]

ADULT_HOBBIES = [
    'アイススケート',
    'アイスホッケー',
    'アウトドア',
    'アニメ鑑賞',
    'アメリカンフットボール',
    'アーチェリー',
    'ウィンドサーフィン',
    'ウェイトリフティング',
    'カヌー',
    'カヤッキング',
    'カラオケ',
    'カーリング',
    'クライミング',
    'コスプレ',
    'ゴルフ',
    'サイクリング',
    'サッカー',
    'サバイバルゲーム',
    'サーフィン',
    'サーフィン',
    'ジョギング',
    'スカッシュ',
    'スキー',
    'スキー',
    'スクーター',
    'スケッチ',
    'スケートボーディング',
    'ストリートバスケットボール',
    'スノーボード',
    'スノーボード',
    'ソフトボール',
    'ダンス',
    'テコンドー',
    'テニス',
    'トライアスロン',
    'ハイキング',
    'ハンググライディング',
    'ハンドボール',
    'ハンドボール',
    'バイアスロン',
    'バスケットボール',
    'バドミントン',
    'バレーボール',
    'バードウォッチング',
    'パズル',
    'パラグライディング',
    'ビデオゲーム',
    'ビーエムエックス',
    'フィギュアスケート',
    'フェンシング',
    'ペットの世話',
    'ボウリング',
    'ボクシング',
    'ボルダリング',
    'ボードゲーム',
    'マラソン',
    'マンガ',
    'ヨガ',
    'ヨット',
    'ラグビー',
    'ラジコン',
    'レーシング',
    'ロッククライミング',
    '体操',
    '写真撮影',
    '切手収集',
    '剣道',
    '卓球',
    '合気道',
    '園芸',
    '弓道',
    '手芸',
    '描画',
    '料理',
    '旅行',
    '日本史',
    '星観察',
    '映画鑑賞',
    '書道',
    '柔道',
    '楽器演奏',
    '水泳',
    '登山',
    '相撲',
    '着物着付け',
    '空手',
    '競馬',
    '自動車乗り',
    '自転車競技',
    '花火大会',
    '茶道',
    '読書',
    '野球',
    '野鳥観察',
    '釣り',
    '鉄道模型',
    '陶芸',
    '陸上',
    '陸上競技',
    '音楽鑑賞',
]

FOODS = [
    'うどん',
    'おせち料理',
    'おでん',
    'おにぎり',
    'お好み焼き',
    'お好み焼き',
    'お茶漬け',
    'かき氷',
    'さしみ',
    'ざるそば',
    'しゃぶしゃぶ',
    'しんじょ',
    'すき焼き',
    'そば',
    'そば湯',
    'だんご汁',
    'とんかつ',
    'なめこ汁',
    'ひつまぶし',
    'わらび餅',
    'アイスクリーム',
    'イカ踊り焼き',
    'インスタントラーメン',
    'エビフライ',
    'カステラ',
    'カツサンド',
    'カツサンド',
    'カツ丼',
    'カリフォルニアロール',
    'カレーライス',
    'クッキー',
    'クリームシチュー',
    'クレープ',
    'クレープスズマ',
    'ケーキ',
    'コロッケ',
    'サラダ',
    'サンドイッチ',
    'ショートケーキ',
    'シーフード',
    'シーフードカレー',
    'シーフードパスタ',
    'ジェラート',
    'スイートポテト',
    'ステーキ',
    'タコス',
    'タルト',
    'チュロス',
    'チョコバナナ',
    'チョコフォンデュ',
    'チョコミント',
    'チョコレート',
    'チーズケーキ',
    'ドーナツ',
    'ハンバーガー',
    'ハンバーガーステーキ',
    'バーガー',
    'パイ',
    'パスタ',
    'パフェ',
    'パンケーキ',
    'ビーフシチュー',
    'ピザ',
    'ピザトースト',
    'フライドチキン',
    'フレンチフライ',
    'プリン',
    'プリンアラモード',
    'ホットドッグ',
    'ホットパン',
    'マカロン',
    'マフィン',
    'モンブラン',
    'ラーメン',
    'ラーメン屋のラーメン',
    'ワッフル',
    '串カツ',
    '丼もの',
    '和菓子',
    '大福',
    '天ぷら',
    '寄せ鍋',
    '寿司',
    '寿司巻き',
    '炭火焼き肉',
    '焼き設け',
    '焼き魚',
    '焼き鳥',
    '焼肉',
    '玉子焼き',
    '生姜焼き',
    '田作',
    '白子丼',
    '石焼きビビンバ',
    '蒸し鶏',
    '親子丼',
    '豆腐',
    '豚汁',
    '餃子',
    '鰻丼',
]

DRINKS = [
    'あたたかい水',
    'ほうじ茶ラテ',
    'アサイージュース',
    'アセロラジュース',
    'アップルジュース',
    'イチゴジュース',
    'ウーロン茶',
    'オレンジジュース',
    'カシスオレンジ',
    'カフェラテ',
    'ガムシロップ',
    'キウイジュース',
    'グアバジュース',
    'グレープジュース',
    'ココア',
    'コーヒー',
    'スムージー',
    'ゼロコーラ',
    'ソフトドリンク',
    'ダージリンティー',
    'チャイ',
    'トロピカルジンジャーティー',
    'ハーブティー',
    'パイナップルジュース',
    'パッションフルーツジュース',
    'ペパーミントティー',
    'マンゴージュース',
    'ミルクティー',
    'レモンティー',
    '三重あまおうジュース',
    '京都アイスコーヒー',
    '北海道牛乳',
    '宇治抹茶',
    '岩清水',
    '火入れ蜜柑',
    '炭酸水',
    '烏龍茶',
    '無糖ソーダ',
    '石垣島パインジュース',
    '米麦茶',
    '紅茶',
    '紅茶ラテ',
    '紫イモバブルティー',
    '緑茶',
    '蜜柑ジュース',
    '赤ブドウジュース',
    '野菜ジュース',
    '金時茶',
    '雪見だいふく',
    '霧島炭酸水',
]

CHILDRENS_PERSONAL_FEATURES = [
    'あまり考えません。',
    'おおらかです。',
    'おしゃべりです。',
    'おなかが弱いです。',
    'くじけません。',
    'けがをしやすいです。',
    'さっぱりしています。',
    'しっかり者です。',
    'しゃべるのが好きです。',
    'すぐに仲良くなります。',
    'すぐに動揺します。',
    'すぐに安心します。',
    'すぐに怖がります。',
    'すぐに感動します。',
    'すぐに泣きます。',
    'すぐに笑います。',
    'すぐに飽きます。',
    'すぐに驚きます。',
    'まつ毛が長いです。',
    'よくくしゃみをします。',
    'よく怒られます。',
    'よく感激します。',
    'よく手伝います。',
    'よく泣きます。',
    'よく目が覚めます。',
    'よく眠ります。',
    'よく笑います。',
    'よく考えます。',
    'よく転びます。',
    'よく遊びます。',
    'よく鼻血が出ます。',
    'アレルギーがあります。',
    'ガチャガチャしています。',
    'ストレスに弱いです。',
    'ネガティブです。',
    'パニックになりやすいです。',
    'ポジティブです。',
    'リラックスするのが難しいです。',
    'ルールを守ります。',
    'ルールを破りがちです。',
    '両親と住んでいます。',
    '人前で話すのが苦手です。',
    '他人に優しいです。',
    '体が丈夫です。',
    '体が柔らかいです。',
    '体が硬いです。',
    '体温が低いです。',
    '体重が軽いです。',
    '優柔不断です。 (I am indecisive.)',
    '元気がいっぱいです。',
    '兄がいます。',
    '具体的です。',
    '冒険心があります。',
    '冷静です。',
    '分析的です。 (I am analytical.)',
    '動きが速いです。',
    '動物が好きです。',
    '友達が多いです。',
    '右利きです。',
    '喘息があります。',
    '喜怒哀楽がはっきりしています。 (I have clear emotions.)',
    '嘘をつきません。',
    '嘘をつくことがあります。',
    '声がかれやすいです.(I have a voice that gets hoarse easily.)',
    '声が小さいです。',
    '声が高いです。',
    '外に出るのが好きです。',
    '夜が得意です。',
    '夢想家です。 (I am a dreamer.)',
    '大胆です。',
    '太りやすいです。',
    '好奇心が強いです。',
    '好奇心旺盛です。',
    '妹がいます。',
    '姉がいます。',
    '孤独が好きです。',
    '家族が大好きです。',
    '家族に愛されています。',
    '寂しがり屋です。',
    '寝付きが悪いです。',
    '少し内気です。',
    '少し曖昧です。',
    '左利きです。',
    '幸福感があります。',
    '弟がいます。',
    '心配ばかりしています。',
    '心配性です。',
    '怒りっぽいです。 (I am quick-tempered.)',
    '怒りやすいです。',
    '怒るのが遅いです。 (I am slow to anger.)',
    '思いやりがあります。',
    '恥ずかしがり屋です。',
    '悲観的です。',
    '想像力が豊かです。 (I am imaginative.)',
    '意地っ張りです。',
    '意思が強いです。',
    '愛されたいです。',
    '感じやすいです。',
    '感動屋です。',
    '感受性が強いです。',
    '感情が豊かです。',
    '感情を隠します。',
    '慎重すぎます。',
    '慎重です。',
    '慎重です。 (I am prudent.)',
    '手が冷えやすいです。',
    '手が器用です。',
    '手が大きいです。',
    '手足が冷え性です。',
    '整理整頓が得意です。',
    '日焼けしやすいです。',
    '時々おねしょをします。',
    '朝が苦手です。',
    '楽観的です。',
    '歌うのが上手です。',
    '正直です。',
    '歩くのが好きです。',
    '歩くのが早いです。',
    '歯がきれいです。',
    '歯が丈夫です。',
    '気まぐれです。',
    '気分屋です。 (I am moody.)',
    '気楽な性格です。',
    '気難しいです。 (I am difficult to please.)',
    '汗をかきやすいです。',
    '決断力が強いです。 (I am decisive.)',
    '消極的です。',
    '無口です。',
    '爪をかむ癖があります。',
    '片付けが苦手です。',
    '物覚えがよいです。',
    '物覚えが悪いです.(I have a poor memory.)',
    '物静かです。',
    '独り言が多いです。',
    '現実的です。 (I am realistic.)',
    '病気にかかりやすいです。',
    '病院に通っています。',
    '痩せやすいです。',
    '登るのが得意です。',
    '皮膚が敏感です。',
    '目が大きいです。',
    '目が悪いです。',
    '目覚めが早いです。',
    '直感が鋭いです。',
    '直感的です。',
    '眉毛が濃いです。',
    '真剣です。',
    '知りたがりです。 (I am inquisitive.)',
    '知ることが好きです。 (I like to know things.)',
    '祖父母がいます。',
    '積極的です。',
    '穏やかです。 (I am calm.)',
    '笑うのが好きです。',
    '笑顔が多いです。',
    '筋肉が付きやすいです。',
    '素直です。',
    '絵を描くのが好きです。',
    '考えすぎます。 (I overthink.)',
    '耳が大きいです。',
    '耳が小さいです。',
    '肌が白いです。',
    '肩が凝りやすいです。',
    '背が高いです。',
    '背中がよく痛みます。',
    '腕が長いです。',
    '自然が好きです。',
    '落ち着きがないです。',
    '親友がいます。',
    '観察力があります。 (I am observant.)',
    '話しかけるのが好きです。',
    '話すのが上手です。',
    '話すのが早いです。',
    '豪快です。 (I am bold.)',
    '負けず嫌いです。',
    '責任感があります。',
    '賢いです。 (I am smart.)',
    '走るのが好きです。',
    '走るのが得意です。',
    '足がよくつるいます。',
    '足が速いです。',
    '足が長いです。',
    '遅寝遅起きです。',
    '陽気です。',
    '集中力があります。',
    '静かな時間が好きです.(I like quiet time.)',
    '面倒見がいいです。',
    '面白がり屋です。',
    '頭が大きいです。',
    '頭痛がよく起こります。',
    '顔が丸いです。',
    '風邪をひきやすいです。',
    '騒ぐのが好きです。',
    '骨が折れやすいです。',
    '髪が短いです。',
    '髪が長いです。',
    '髪が黒いです。',
    '鼻が低いです。',
    '鼻が敏感です。',
    '鼻が高いです。',
    '鼻水がよく出ます。',
]

ADULTS_PERSONAL_FEATURES = [
    'うつ病があります。',
    'えくぼがあります。',
    'おおざっぱです。',
    'おおらかです。',
    'かすれた声があります。',
    'かまってくれる人が好きです。',
    'くせ毛です。',
    'しつこいです。',
    'すぐに怒ります。',
    'そばかすがあります。',
    'ぞくぞくします。',
    'たくさんの友達がいます。',
    'ちりめんじわがあります。',
    'ひとりの時間が好きです。',
    'やさしいです。',
    'アトピー性皮膚炎があります。',
    'アレルギーがあります。',
    'インスリンを注射します。',
    'エイズ患者です。',
    'オプティミストです。',
    'ストイックです。',
    'スポーツが得意です。',
    'セルライトがあります。',
    'ソシオパスです。',
    'トランスジェンダーです。',
    'ナルシシストです。',
    'パニック障害があります。',
    'ピアスをしているです。',
    'プライベートを大切にします。',
    'ペシミストです。',
    'ペースメーカーを持っています。',
    'マイペースです。',
    '一人っ子です。',
    '一人暮らしです。',
    '一度結婚経験があります。',
    '一重まぶたです。',
    '三つ子です。',
    '三人兄弟の末っ子です。',
    '三度の手術を受けました。',
    '不安症です。',
    '両性愛者です。',
    '両親と一緒に住んでいます。',
    '中肉中背です。',
    '丸いお尻があります。',
    '丸い顔です。',
    '乱暴です。',
    '乳糖不耐症があります。',
    '乾燥性湿疹があります。',
    '乾燥肌です。',
    '二人子供があります。',
    '二重まぶたです。',
    '人の感情を考慮します。',
    '人の話をよく聞きます。',
    '人を判断しがちです。',
    '人懐っこいです。',
    '人見知りです。',
    '人間関係が苦手です。',
    '他の人の意見を尊重します。',
    '仲間意識が強いです。',
    '似顔絵を描くのが得意です。',
    '低血圧です。',
    '体温が低いです。',
    '体温が高めです。',
    '体温調節が難しいです。',
    '保守的な家庭で育ちました。',
    '信仰深いです。',
    '信頼しやすいです。',
    '健忘症です。',
    '優しさに欠けます。',
    '優柔不断です。',
    '兄弟姉妹がいません。',
    '光に敏感です。',
    '免疫力が強いです。',
    '入れ歯があります。',
    '公平です。',
    '共感力があります。',
    '共感能力があります。',
    '内向的です。',
    '内気です。',
    '内省的です。',
    '内臓疾患があります。',
    '再婚しました。',
    '冒険心があります。',
    '冷淡です。',
    '冷静です。',
    '几帳面です。',
    '分析的です。',
    '利己的です。',
    '刺青があります。',
    '劣等感があります。',
    '助けを求めるのが苦手です。',
    '励まされやすいです。',
    '動物に過敏です。',
    '協力性があります。',
    '協調性があります。',
    '協調性に欠けます。',
    '協調的です。',
    '博愛主義者です。',
    '即興で行動するのが好きです。',
    '即興性があります。',
    '厚い唇があります。',
    '厳しいです。',
    '友好的です。',
    '友達が少ないです。',
    '双子です。',
    '双極性障害があります。',
    '口が軽いです。',
    '口内炎が出やすいです。',
    '口唇ヘルペスがあります。',
    '口数が少ないです。',
    '右利きです。',
    '同性愛者です。',
    '否定的です。',
    '唇が乾燥しやすいです。',
    '喘息があります。',
    '四肢麻痺です。',
    '堅実です。',
    '声がかすれがちです。',
    '声が低いです。',
    '声が高いです。',
    '外向的です。',
    '夢見がちです。',
    '大きい耳です。',
    '大きな口を持っています。',
    '大きな手があります。',
    '大きな足があります。',
    '大声が苦手です。',
    '大胆です。',
    '大胆不敵です。',
    '太い首です。',
    '太っているです。',
    '好奇心が強いです。',
    '好奇心が旺盛です。',
    '好奇心旺盛です。',
    '姪があります。',
    '嫉妬深いです。',
    '孤独を感じやすいです。',
    '孤立しがちです。',
    '孤高です。',
    '学者気質です。',
    '完全主義者です。',
    '完璧主義者です。',
    '実務的です。',
    '寂しがり屋です。',
    '寛大です。',
    '小さい手です。',
    '小さい足です。',
    '小さい鼻です。',
    '小さな口です。',
    '少々頑固です。',
    '左利きです。',
    '左目が義眼です。',
    '巻き髪です。',
    '広い肩幅です。',
    '引きこもりがちです。',
    '引っ込み思案です。',
    '弱視です。',
    '強迫性障害があります。',
    '弾力のある肌です。',
    '律儀です。',
    '心が乱れやすいです。',
    '心臓病があります。',
    '心配事が多いです。',
    '心配性です。',
    '忍耐力があります。',
    '忍耐強いです。',
    '快楽主義者です。',
    '快活です。',
    '思いやりがあります。',
    '思い出にふけりやすいです。',
    '怠け者です。',
    '急進的です。',
    '性別違和があります。',
    '悠長です。',
    '悪夢を見やすいです。',
    '悲観主義者です。',
    '悲観的です。',
    '情け深いです。',
    '情熱家です。',
    '情熱的です。',
    '情緒的です。',
    '愛想がいいです。',
    '愛想笑いが得意です。',
    '感動しやすいです。',
    '感受性が敏感です。',
    '感受性が豊かです。',
    '感情が表に出やすいです。',
    '感情的です。',
    '感謝の心を忘れません。',
    '慎重です。',
    '慢性偏頭痛があります。',
    '憂鬱な気持ちがあります。',
    '批判的です。',
    '持久力があります。',
    '持久力がありません。',
    '摂食障害があります。',
    '敏感肌を持っています。',
    '文盲です。',
    '料理が得意です。',
    '新しいことに挑戦するのが好きです。',
    '新潟しました。',
    '方向音痴です。',
    '日焼けしやすいです。',
    '未婚です。',
    '柔軟です。',
    '根気があります。',
    '極端に正直です。',
    '楽天主義です。',
    '楽天的です。',
    '楽観主義です。',
    '楽観主義者です。',
    '楽観的です。',
    '機知に富んでいます。',
    '正直です。',
    '歯ぎしりをします。',
    '毅然としています。',
    '気が短いです。',
    '気まぐれです。',
    '気むずかしいです。',
    '気前が良いです。',
    '水が怖いです。',
    '注意欠陥多動性障害があります。',
    '洞察力があります。',
    '消化不良がよくあります。',
    '涙もろいです。',
    '潔癖症です。',
    '無性愛者です。',
    '無愛想です。',
    '無礼です。',
    '無謀です。',
    '無関心です。',
    '熱射病になりやすいです。',
    '熱心です。',
    '爪噛み癖があります。',
    '片耳が聞こえません。',
    '片腕です。',
    '片頭痛があります。',
    '物を捨てられません。',
    '物静かです。',
    '物静かな性格です。',
    '犠牲的な性格です。',
    '献身的です。',
    '現実主義です。',
    '理性的です。',
    '生まれつきのリーダーです。',
    '異性愛者です。',
    '疑います。',
    '疑り深いです。',
    '痩せています。',
    '白髪が多いです。',
    '目が青いです。',
    '盲目です。',
    '直感型です。',
    '直毛です。',
    '直観的です。',
    '眉毛が濃いです。',
    '睡眠障害があります。',
    '矛盾しています。',
    '短い足です。',
    '短気です。',
    '礼儀正しいです。',
    '社交不安があります。',
    '社交不安症です。',
    '社交的です。',
    '祖母と一緒に住んでいます。',
    '秘密を守ります。',
    '穏やかな性格です。',
    '空間認識が良いです。',
    '笑うことが大好きです。',
    '筋肉疲労があります。',
    '筋肉質です。',
    '糖尿病です。',
    '細い肩です。',
    '細い腕があります。',
    '細い腰です。',
    '細面です。',
    '統合失調症があります。',
    '緊張すると汗っかきです。',
    '緻密です。',
    '義侠心があります。',
    '義理堅いです。',
    '義足を持っています。',
    '耳が小さいです。',
    '耳が聞こえません。',
    '耳鳴りがあります。',
    '聞き上手です。',
    '肌にトラブルがあります。',
    '胃腸が弱いです。',
    '背が低いです。',
    '背が高いです。',
    '胸が大きいです。',
    '胸が小さいです。',
    '脂肌です。',
    '脊椎側弯症があります。',
    '脊髄炎を患っています。',
    '腎臓病があります。',
    '膀胱炎になりやすいです。',
    '臆病です。',
    '自信があります。',
    '自信がないです。',
    '自信過剰です。',
    '自分の意見が強いです。',
    '自尊心があります。',
    '自己中心的です。',
    '自己主張が強いです。',
    '自己卑下しやすいです。',
    '自己犠牲的です。',
    '自慢話が多いです。',
    '自立しています。',
    '自閉症スペクトラムです。',
    '色白です。',
    '花粉症があります。',
    '芸術肌です。',
    '薄い眉毛です。',
    '虫が苦手です。',
    '蛇行疹が出やすいです。',
    '融通が効かないです。',
    '血友病があります。',
    '血液が固まりにくいです。',
    '行動力があります。',
    '衝動的です。',
    '表現力豊かです。',
    '親孝行です。',
    '角刈りです。',
    '解離性障害があります。',
    '計画が立てるのが得意です。',
    '計画性がありません。',
    '計画性に欠けます。',
    '計算高いです。',
    '話し下手です。',
    '話し好きです。',
    '誇り高いです。',
    '誇張して話すのが好きです。',
    '誠実です。',
    '誠実な人間です。',
    '謎めいた性格です。',
    '謙虚です。',
    '議論好きです。',
    '貧血です。',
    '責任感があります。',
    '赤面しやすいです。',
    '足が長いです。',
    '躁うつ障害があります。',
    '車椅子を使っています。',
    '辛抱強いです。',
    '近くの音が聞こえにくいです。',
    '近視です。',
    '速い代謝を持っています。',
    '遅い代謝を持っています。',
    '過去にいじめられた経験があります。',
    '過去を後悔しています。',
    '過敏性腸症候群があります。',
    '野心家です。',
    '鋭い観察力があります。',
    '鋭敏です。',
    '錯乱しやすいです。',
    '長い指があります。',
    '長女です。',
    '長男です。',
    '閉所恐怖症です。',
    '開放的な家族に育ちました。',
    '関節痛に悩まされています。',
    '集団行動が苦手です。',
    '難聴です。',
    '青白い肌です。',
    '音楽のリズムに敏感です。',
    '額が広いです。',
    '顎が尖っています。',
    '高さが怖いです。',
    '高血圧です。',
    '髪の毛が薄いです。',
    '髪の毛が黒いです。',
    '鼻が高いです。',
    '鼻血が出やすいです。',
]

MOODS = [
    'がっかりしています。',
    'イライラしています。',
    'ジェラシーを感じています。',
    'リラックスしています。',
    '不安です。',
    '信じています。',
    '冷静です。',
    '刺激されています。',
    '刺激されています。',
    '刺激を求めています。',
    '失望しています。',
    '好奇心が強いです。',
    '孤独を感じています。',
    '希望しています。',
    '平和です。',
    '幸せです。',
    '弱いです。',
    '強いです。',
    '心配しています。',
    '怒っています。',
    '怖がっています。',
    '恐れています。',
    '恥ずかしいです。',
    '悔いています。',
    '悲しいです。',
    '意欲的です。',
    '感動しています。',
    '感謝しています。',
    '慌てています。',
    '憤慨しています。',
    '懐疑的です。',
    '楽しんでいます。',
    '活動的です。',
    '混乱しています。',
    '満足しています。',
    '無精です。',
    '焦っています。',
    '熱狂しています。',
    '甘やかされています。',
    '疑っています。',
    '疲れています。',
    '確信しています。',
    '穏やかです。',
    '緊張しています。',
    '興奮しています。',
    '興奮しています。',
    '落ち込んでいます。',
    '静かです。',
    '騒がしいです。',
    '驚いています。',
]


def get_random_age() -> int:
    return random.randint(MIN_AGE, MAX_AGE)  # nosec


def get_random_name(male: bool) -> str:
    family_name = FAMILY_NAMES[random.randint(0, len(FAMILY_NAMES) - 1)]  # nosec
    if male:
        first_name = MALE_NAMES[random.randint(0, len(MALE_NAMES) - 1)]  # nosec
    else:
        first_name = FEMALE_NAMES[random.randint(0, len(FEMALE_NAMES) - 1)]  # nosec
    return f'{family_name}{first_name}'


def get_random_city() -> str:
    return CITIES[random.randint(0, len(CITIES) - 1)]  # nosec


def get_random_profession(age: int) -> str:
    match age:
        case age if 0 <= age < 3:
            return 'ママとずっと一緒にいる赤ちゃん'
        case age if 3 <= age < 6:
            return '幼稚園生'
        case age if 6 <= age < 12:
            return '小学生'
        case age if 12 <= age < 15:
            return '中学生'
        case age if 15 <= age < 18:
            return '高校生'
        case age if 18 <= age < 21:
            if random.choice([True, False, False]):  # nosec
                return '大学生'
    return PROFESSIONS[random.randint(0, len(PROFESSIONS) - 1)]  # nosec


def get_random_hobbies(age: int) -> str:
    hobbies = random.sample(  # nosec
        (
            SMALL_CHILDRENS_HOBBIES
            if age < 6
            else BIG_CHILDRENS_HOBBIES
            if age < 13
            else ADOLESCENTS_HOBBIES
        ),
        random.randint(2, 4),  # nosec
    )
    return 'と'.join(hobbies)


def get_random_foods_and_drinks() -> str:
    foods = random.sample(FOODS, random.randint(1, 2))  # nosec
    drinks = random.sample(DRINKS, random.randint(1, 2))  # nosec
    return 'や'.join(foods + drinks)


def get_random_personal_feature(age: int) -> str:
    if age < 18:
        return CHILDRENS_PERSONAL_FEATURES[
            random.randint(0, len(CHILDRENS_PERSONAL_FEATURES) - 1)  # nosec
        ]
    return ADULTS_PERSONAL_FEATURES[
        random.randint(0, len(ADULTS_PERSONAL_FEATURES) - 1)  # nosec
    ]


def get_random_mood() -> str:
    return MOODS[random.randint(0, len(MOODS) - 1)]  # nosec


def get_pitch(male: bool, age: int) -> float:
    assert MIN_AGE <= age <= MAX_AGE
    match age:
        case age if age < 18:
            x1, y1 = (
                MIN_AGE,
                (
                    MALE_PITCH_CHANGE_SEMITONES
                    if male
                    else FEMALE_PITCH_CHANGE_SEMITONES
                ),
            )
            x2, y2 = 18, 0
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            return m * age + b
        case age if 18 <= age < 40:
            return 0
        case _:
            x1, y1 = 40, 0
            x2, y2 = MAX_AGE, -20
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            return m * age + b


def test_get_pitch(male: bool, age: int, expected: float) -> None:
    pitch = get_pitch(male, age)
    assert round(pitch, 1) == expected, f'{age}: {round(pitch, 1)} != {expected}'


male = True
test_get_pitch(male, 3, 12)
test_get_pitch(male, 4, 11.2)
test_get_pitch(male, 10, 6.4)
test_get_pitch(male, 14, 3.2)
test_get_pitch(male, 18, 0)
test_get_pitch(male, 25, 0)
test_get_pitch(male, 39, 0)
test_get_pitch(male, 40, 0)
test_get_pitch(male, 45, -5)
test_get_pitch(male, 50, -10)
test_get_pitch(male, 60, -20)
male = False
test_get_pitch(male, 3, 6)
test_get_pitch(male, 4, 5.6)
test_get_pitch(male, 10, 3.2)
test_get_pitch(male, 14, 1.6)
test_get_pitch(male, 18, 0)
test_get_pitch(male, 25, 0)
test_get_pitch(male, 39, 0)
test_get_pitch(male, 40, 0)
test_get_pitch(male, 45, -5)
test_get_pitch(male, 50, -10)
test_get_pitch(male, 60, -20)


def get_random_speaking_rate() -> float:
    return random.uniform(0.7, 1.0)  # nosec
