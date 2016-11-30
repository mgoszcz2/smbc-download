-- smbc-download - Download top 100 comics from smbc
-- Copyright (C) 2016 Maciej Goszczycki
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.

-- You should have received a copy of the GNU General Public License
-- along with this program.  If not, see <http://www.gnu.org/licenses/>.

import Text.HandsomeSoup
import Text.XML.HXT.Core
import Control.Monad.Trans.Maybe
import System.FilePath.Posix
import Data.Maybe
import Control.Monad
import System.Directory
import System.IO


downloadComic :: String -> IO ()
downloadComic name = do
    let smbcComic = "http://www.smbc-comics.com/comic/"
    url <- runX $ fromUrl (smbcComic ++ name) >>> css "#cc-comic" ! "src"
    let fname = "smbc/" ++ name ++ takeExtension (head url)
    exists <- doesFileExist fname
    if exists then putStrLn $ "Skipping " ++ fname
    else do
        putStrLn $ "Downloading " ++ fname
        contents <- runMaybeT . openUrl $ head url
        writeFile fname $ fromJust contents
    hFlush stdout

main :: IO ()
main = do
    let smbcArchive = "http://www.smbc-comics.com/comic/archive/"
    links <- runX $ fromUrl smbcArchive >>> css "option" ! "value" >>. filter (not . null)
    createDirectoryIfMissing False "smbc"
    putStrLn "Downloading into smbc/"
    mapM_ downloadComic $ take 100 links
