CREATE TABLE IF NOT EXISTS `user` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL,
  `numero` varchar(200) NOT NULL,
  `role` varchar(200) NOT NULL DEFAULT 'member',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
);

INSERT INTO user (name, email, password, numero, role)
VALUES 
('Florent Ibanez', 'florent.ibanez@gmail.com', '97c21baef3973c46daf3213f2a8198e8135e62001871fda79267f9dda0f5626d', '+33 7 84 62 19 67', 'admin'),
('Wassim Ahmed-Belkacem', 'wassim.ahmed-belkacem@gmail.com', 'ec4e3bfaf8682b6933ab10550bc4ba20ce09024b642def9a258f9b9db1ce52e5', '+33 6 57 18 94 75', 'member'),
('Emie Delepine', 'emie.delepine@gmail.com', '7faf5f63eace4a29b04d494670934552e19b99d2a75cd8dcb76a29fd2e80a10d', '+33 6 31 87 94 25', 'member'),
('Cyan Huet', 'cyan.huet@gmail.com', 'a4b9a0e1e59584d1c8e2667250a5274bbd35eda80167ac247065a70da31d92b1', '+33 6 94 10 18 47', 'member');