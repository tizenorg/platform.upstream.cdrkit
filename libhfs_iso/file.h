/*
 * This file has been modified for the cdrkit suite.
 *
 * The behaviour and appearence of the program code below can differ to a major
 * extent from the version distributed by the original author(s).
 *
 * For details, see Changelog file distributed with the cdrkit package. If you
 * received this file from another source then ask the distributing person for
 * a log of modifications.
 *
 */

/* @(#)file.h	1.1 00/03/05 joerg */
/*
 * hfsutils - tools for reading and writing Macintosh HFS volumes
 * Copyright (C) 1996, 1997 Robert Leslie
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 */

enum {
  fkData = 0x00,
  fkRsrc = 0xff
};

void f_selectfork(hfsfile *, int);
void f_getptrs(hfsfile *, unsigned long **, unsigned long **, ExtDataRec **);

int f_doblock(hfsfile *, unsigned long, block *, 
				  int (*)(hfsvol *, unsigned int, unsigned int, block *));

# define f_getblock(file, num, bp)	f_doblock(file, num, bp, b_readab)
# define f_putblock(file, num, bp)	f_doblock(file, num, bp, b_writeab)

int f_alloc(hfsfile *);
int f_flush(hfsfile *);
