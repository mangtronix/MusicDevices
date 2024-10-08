FasdUAS 1.101.10   ��   ��    k             l     ��  ��    8 2 Automatically click Connect for a BLE MIDI device     � 	 	 d   A u t o m a t i c a l l y   c l i c k   C o n n e c t   f o r   a   B L E   M I D I   d e v i c e   
  
 l     ��  ��    ' ! Runs in a loop - hit stop to end     �   B   R u n s   i n   a   l o o p   -   h i t   s t o p   t o   e n d      l     ��������  ��  ��        l     ��  ��    6 0 The Bluetooth Configuration window must be open     �   `   T h e   B l u e t o o t h   C o n f i g u r a t i o n   w i n d o w   m u s t   b e   o p e n      l     ��  ��    D >   Audio MIDI Setup->MIDI Studio->Open Bluetooth Configuration     �   |       A u d i o   M I D I   S e t u p - > M I D I   S t u d i o - > O p e n   B l u e t o o t h   C o n f i g u r a t i o n      l     ��  ��    5 / Enter the device name below and run the script     �   ^   E n t e r   t h e   d e v i c e   n a m e   b e l o w   a n d   r u n   t h e   s c r i p t     !   l     �� " #��   " O I Accessibility control must be enabled for the script to click the button    # � $ $ �   A c c e s s i b i l i t y   c o n t r o l   m u s t   b e   e n a b l e d   f o r   t h e   s c r i p t   t o   c l i c k   t h e   b u t t o n !  % & % l     ��������  ��  ��   &  ' ( ' l     �� ) *��   )   Written with ChatGPT    * � + + *   W r i t t e n   w i t h   C h a t G P T (  , - , l     �� . /��   .   Michael Ang @mangtronix    / � 0 0 0   M i c h a e l   A n g   @ m a n g t r o n i x -  1 2 1 l     �� 3 4��   3   2024-04    4 � 5 5    2 0 2 4 - 0 4 2  6 7 6 l     ��������  ��  ��   7  8 9 8 l     ��������  ��  ��   9  : ; : l     ��������  ��  ��   ;  < = < l      > ? @ > j     �� A�� *0 devicenametoconnect deviceNameToConnect A m      B B � C C  M u s i c D e v i c e s ?    Set your device name here    @ � D D 4   S e t   y o u r   d e v i c e   n a m e   h e r e =  E F E l      G H I G j    �� J��  0 repeatinterval repeatInterval J m    ����  H 3 - Set the repeat time interval in seconds here    I � K K Z   S e t   t h e   r e p e a t   t i m e   i n t e r v a l   i n   s e c o n d s   h e r e F  L M L l      N O P N j    �� Q�� 00 alreadyconnectedlogged alreadyConnectedLogged Q m    ��
�� boovfals O 4 . Tracks if "already connected" has been logged    P � R R \   T r a c k s   i f   " a l r e a d y   c o n n e c t e d "   h a s   b e e n   l o g g e d M  S T S l     ��������  ��  ��   T  U V U i   	  W X W I     ������
�� .aevtoappnull  �   � ****��  ��   X k    V Y Y  Z [ Z l    
 \ ] ^ \ O    
 _ ` _ I   	������
�� .miscactvnull��� ��� null��  ��   ` m      a a�                                                                                  AMDS  alis    j  Macintosh HD               �!��BD ����Audio MIDI Setup.app                                           �����!��        ����  
 cu             	Utilities   5/:System:Applications:Utilities:Audio MIDI Setup.app/   *  A u d i o   M I D I   S e t u p . a p p    M a c i n t o s h   H D  2System/Applications/Utilities/Audio MIDI Setup.app  / ��   ] ' ! Ensure the application is active    ^ � b b B   E n s u r e   t h e   a p p l i c a t i o n   i s   a c t i v e [  c d c l    e f g e I   �� h��
�� .sysodelanull��� ��� nmbr h m    ���� ��   f M G Wait a couple of seconds for the application to come to the foreground    g � i i �   W a i t   a   c o u p l e   o f   s e c o n d s   f o r   t h e   a p p l i c a t i o n   t o   c o m e   t o   t h e   f o r e g r o u n d d  j k j l   ��������  ��  ��   k  l�� l T   V m m O   Q n o n O   P p q p k   !O r r  s t s l  ! !�� u v��   u !  Check if the window exists    v � w w 6   C h e c k   i f   t h e   w i n d o w   e x i s t s t  x y x Z   !E z {�� | z I  ! )�� }��
�� .coredoexnull���     **** } 4   ! %�� ~
�� 
cwin ~ m   # $   � � � . B l u e t o o t h   C o n f i g u r a t i o n��   { k   ,; � �  � � � l  , ,�� � ���   �   set frontmost to true    � � � � ,   s e t   f r o n t m o s t   t o   t r u e �  ��� � O   ,; � � � O   3: � � � O   :9 � � � k   A8 � �  � � � r   A D � � � m   A B��
�� boovfals � o      ���� 0 devicefound deviceFound �  � � � r   E H � � � m   E F��
�� boovfals � o      ���� 0 buttonclicked buttonClicked �  � � � Y   I � ��� � ��� � k   Y � � �  � � � r   Y a � � � 4   Y ]�� �
�� 
crow � o   [ \���� 0 i   � o      ���� 0 
currentrow 
currentRow �  � � � l  b b�� � ���   � S M Check if the row contains the device name specified by `deviceNameToConnect`    � � � � �   C h e c k   i f   t h e   r o w   c o n t a i n s   t h e   d e v i c e   n a m e   s p e c i f i e d   b y   ` d e v i c e N a m e T o C o n n e c t ` �  ��� � Z   b � � ����� � =  b y � � � n   b s � � � 1   o s��
�� 
valL � n   b o � � � 4   j o�� �
�� 
sttx � m   m n����  � n   b j � � � 4   e j�� �
�� 
uiel � m   h i����  � o   b e���� 0 
currentrow 
currentRow � o   s x���� *0 devicenametoconnect deviceNameToConnect � k   | � � �  � � � r   |  � � � m   | }��
�� boovtrue � o      ���� 0 devicefound deviceFound �  � � � l  � ��� � ���   � / ) Check if the cell has a "Connect" button    � � � � R   C h e c k   i f   t h e   c e l l   h a s   a   " C o n n e c t "   b u t t o n �  ��� � O   � � � � � l  � � � � � � k   � � � �  � � � r   � � � � � 2   � ���
�� 
butT � o      ���� 0 
buttonlist 
buttonList �  ��� � Z   � � � � ��� � F   � � � � � >  � � � � � o   � ����� 0 
buttonlist 
buttonList � J   � �����   � l  � � ����� � =  � � � � � n   � � � � � 1   � ���
�� 
pnam � 4   � ��� �
�� 
butT � m   � �����  � m   � � � � � � �  C o n n e c t��  ��   � k   � � � �  � � � I  � ��� ���
�� .prcsclicnull��� ��� uiel � 4   � ��� �
�� 
butT � m   � � � � � � �  C o n n e c t��   �  � � � r   � � � � � m   � ���
�� boovtrue � o      ���� 0 buttonclicked buttonClicked �  � � � I  � ��� ���
�� .ascrcmnt****      � **** � m   � � � � � � �  C o n n e c t i n g��   �  ��� � l  � � � � � �  S   � � � 8 2 Button was found and clicked, no need to continue    � � � � d   B u t t o n   w a s   f o u n d   a n d   c l i c k e d ,   n o   n e e d   t o   c o n t i n u e��   �  � � � H   � � � � o   � ����� 00 alreadyconnectedlogged alreadyConnectedLogged �  ��� � k   � � � �  � � � l  � ��� � ���   �    Log the message only once    � � � � 4   L o g   t h e   m e s s a g e   o n l y   o n c e �  � � � I  � ��� ���
�� .ascrcmnt****      � **** � m   � � � � � � � 0 D e v i c e   a l r e a d y   c o n n e c t e d��   �  ��� � r   � � � � � m   � ���
�� boovtrue � o      ���� 00 alreadyconnectedlogged alreadyConnectedLogged��  ��  ��  ��   � 1 + assuming the button is in the third column    � �   V   a s s u m i n g   t h e   b u t t o n   i s   i n   t h e   t h i r d   c o l u m n � n   � � 4   � ���
�� 
uiel m   � �����  o   � ����� 0 
currentrow 
currentRow��  ��  ��  ��  �� 0 i   � m   L M����  � I  M T����
�� .corecnte****       **** 2  M P��
�� 
crow��  ��   �  l  � �����   6 0 Output the result if the button was not clicked    �		 `   O u t p u t   t h e   r e s u l t   i f   t h e   b u t t o n   w a s   n o t   c l i c k e d 
��
 Z   �8�� F   � F   � o   � ����� 0 devicefound deviceFound H   � � o   � ����� 0 buttonclicked buttonClicked H  
 o  	���� 00 alreadyconnectedlogged alreadyConnectedLogged I ����
�� .ascrcmnt****      � **** m   � ` D e v i c e   f o u n d   b u t   ' C o n n e c t '   b u t t o n   n o t   a v a i l a b l e .��    F  * H   o  ���� 0 devicefound deviceFound H   & o   %���� 00 alreadyconnectedlogged alreadyConnectedLogged �� I -4����
�� .ascrcmnt****      � **** m  -0 �   " D e v i c e   n o t   f o u n d .��  ��  ��  ��   � 4   : >��!
�� 
tabB! m   < =����  � 4   3 7��"
�� 
scra" m   5 6����  � 4   , 0�#
� 
cwin# m   . /$$ �%% . B l u e t o o t h   C o n f i g u r a t i o n��  ��   | I >E�~&�}
�~ .ascrcmnt****      � ****& m  >A'' �(( n B l u e t o o t h   C o n f i g u r a t i o n   w i n d o w   n o t   f o u n d .   T r y i n g   a g a i n .�}   y )*) l FF�|+,�|  + G A Wait for the specified repeat interval before repeating the loop   , �-- �   W a i t   f o r   t h e   s p e c i f i e d   r e p e a t   i n t e r v a l   b e f o r e   r e p e a t i n g   t h e   l o o p* .�{. I FO�z/�y
�z .sysodelanull��� ��� nmbr/ o  FK�x�x  0 repeatinterval repeatInterval�y  �{   q 4    �w0
�w 
pcap0 m    11 �22   A u d i o   M I D I   S e t u p o m    33�                                                                                  sevs  alis    \  Macintosh HD               �!��BD ����System Events.app                                              �����!��        ����  
 cu             CoreServices  0/:System:Library:CoreServices:System Events.app/  $  S y s t e m   E v e n t s . a p p    M a c i n t o s h   H D  -System/Library/CoreServices/System Events.app   / ��  ��   V 4�v4 l     �u�t�s�u  �t  �s  �v       �r5 B�q�p6�r  5 �o�n�m�l�o *0 devicenametoconnect deviceNameToConnect�n  0 repeatinterval repeatInterval�m 00 alreadyconnectedlogged alreadyConnectedLogged
�l .aevtoappnull  �   � ****�q 
�p boovfals6 �k X�j�i78�h
�k .aevtoappnull  �   � ****�j  �i  7 �g�g 0 i  8 ! a�f�e3�d1�c �b$�a�`�_�^�]�\�[�Z�Y�X�W�V�U ��T ��S ��R �'
�f .miscactvnull��� ��� null
�e .sysodelanull��� ��� nmbr
�d 
pcap
�c 
cwin
�b .coredoexnull���     ****
�a 
scra
�` 
tabB�_ 0 devicefound deviceFound�^ 0 buttonclicked buttonClicked
�] 
crow
�\ .corecnte****       ****�[ 0 
currentrow 
currentRow
�Z 
uiel
�Y 
sttx
�X 
valL
�W 
butT�V 0 
buttonlist 
buttonList
�U 
pnam
�T 
bool
�S .prcsclicnull��� ��� uiel
�R .ascrcmnt****      � ****�hW� *j UOlj ODhZ�8*��/0*��/j *��/	*�k/*�k/ �fE�OfE�O �k*�-j kh  *�/E` O_ a k/a k/a ,b     veE�O_ a m/ c*a -E` O_ jv	 *a k/a ,a  a & *a a /j OeE�Oa j OY b   a j OeEc  Y hUY h[OY�bO�	 �a &	 b  a & a j Y �	 b  a & a j Y hUUUY 	a  j Ob  j UU[OY�� ascr  ��ޭ